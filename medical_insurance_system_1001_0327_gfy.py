# 代码生成时间: 2025-10-01 03:27:27
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
import json


# Model for MedicalInsurance
class Patient(models.Model):
    """Patient model to store patient details."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ssn = models.CharField(max_length=11, unique=True)  # Social Security Number
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    """Service model to store services provided to patients."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class InsurancePlan(models.Model):
    """Insurance plan model to store different plans."""
    name = models.CharField(max_length=100)
    coverage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Claim(models.Model):
    """Claim model to store claims made by patients for services."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    plan = models.ForeignKey(InsurancePlan, on_delete=models.CASCADE)
    claim_date = models.DateField(auto_now_add=True)
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Claim {self.id} for {self.patient}"


# View for handling medical insurance claims
class MedicalInsuranceView(View):
    """View to handle medical insurance claims."""
    def post(self, request):
        """Handle POST request to create a new claim."""
        try:
            data = json.loads(request.body)
            patient_ssn = data.get('patient_ssn')
            service_name = data.get('service_name')
            plan_name = data.get('plan_name')
            amount_claimed = data.get('amount_claimed')

            # Find the patient, service, and insurance plan
            patient = Patient.objects.get(ssn=patient_ssn)
            service = Service.objects.get(name=service_name)
            plan = InsurancePlan.objects.get(name=plan_name)

            # Create a new claim
            claim = Claim.objects.create(
                patient=patient,
                service=service,
                plan=plan,
                amount_claimed=amount_claimed
            )

            # Simulate claim approval process (This would be replaced with actual logic)
            claim.amount_approved = claim.amount_claimed * plan.coverage / 100
            claim.save()

            return JsonResponse({'message': 'Claim submitted and approved.', 'claim_id': claim.id})
        except (Patient.DoesNotExist, Service.DoesNotExist, InsurancePlan.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


# URL configuration for the medical insurance view
urlpatterns = [
    path('claim/', csrf_exempt(MedicalInsuranceView.as_view()), name='medical_insurance_claim'),
]
