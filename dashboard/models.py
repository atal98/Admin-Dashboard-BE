from django.db import models

class UsersInfo(models.Model):
    userid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    cr_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_info'

class CategoryOfProducts(models.Model):
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    productid = models.AutoField(primary_key=True)
    product_type = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_of_products'

class ProductInfo(models.Model):
    productid = models.OneToOneField('CategoryOfProducts', models.DO_NOTHING, primary_key=True, db_column='productid', blank=True, null=False)
    cost_type = models.CharField(max_length=50, blank=True, null=True)
    distribution_cost = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    logistics_cost = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    administration_cost = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    marketing_cost = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    cost_making_or_buying = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_info'

class Leads(models.Model):
    year = models.CharField(max_length=4, blank=True, null=True)
    quarter = models.IntegerField(blank=True, null=True)
    ads_leads = models.BigIntegerField(blank=True, null=True)
    email_leads = models.BigIntegerField(blank=True, null=True)
    refferal_leads = models.BigIntegerField(blank=True, null=True)
    social_media = models.BigIntegerField(blank=True, null=True)
    trade_show_leads = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leads'

class SalesAndMarketing(models.Model):
    quarter = models.IntegerField(blank=True, null=True)
    ads = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    salaries = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    content_creation = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    other_expense = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    total_expense = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_and_marketing'


class Transaction(models.Model):
    transactionid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UsersInfo', models.DO_NOTHING, blank=True, null=True)
    productid = models.ForeignKey('CategoryOfProducts', models.DO_NOTHING, db_column='productid', blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class TransactionInfo(models.Model):
    transactionid = models.OneToOneField('Transaction', models.DO_NOTHING, db_column='transactionid', primary_key=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_info'