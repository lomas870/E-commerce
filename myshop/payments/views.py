from django.shortcuts import render,redirect,get_object_or_404
import requests
import json
from core.models import Order
from .models import *
from django.http import JsonResponse
import uuid

# Create your views here.
def initkhalti(request,id):
    data=Order.objects.get(id=id)


    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/payments/verifyKhalti",
        "website_url": "http://127.0.0.1:8000/payments/verifyKhalti",
        "amount": int(float(data.total))*100,
        "purchase_order_id": data.id,
        "purchase_order_name": data.product,
        'transacation_id':str(uuid.uuid4),
        "customer_info": {
        "name": request.user.username,
        "email": request.user.email,
        "phone":request.user.phone
        }
    })
    headers = {
        'Authorization': 'key 8caa44292499411c9f72f6b8f0d43b65',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    payment_url=json.loads(response.text)['payment_url']
    return redirect(payment_url)

def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key  8caa44292499411c9f72f6b8f0d43b65',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            order=get_object_or_404(Order,id=purchase_order_id)
            order.is_pay=True
            order.save()

            Transaction.objects.create(order=order,user=request.user,amount=new_res['total_amount'],transaction_id=transaction_id)
           

           
            return redirect('my_order')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'},status=400)