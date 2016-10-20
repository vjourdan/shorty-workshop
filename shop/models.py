# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Nom de la Catégorie')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return u'%s : %s' % (_('Category'), self.name)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Nom du produit')
    content = models.TextField(verbose_name=u'Description', blank=True)
    price = models.FloatField(verbose_name=u'Prix d\'achat')
    categories = models.ManyToManyField(Category, verbose_name=u'Catégories')

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return u' '.join([self.name, str(self.price), self.get_categories()])

    def get_categories(self):
        return u', '.join([obj.name for obj in self.categories.all()])
    get_categories.short_description = "Categories"


class ProductImage(models.Model):
    image = models.ImageField(verbose_name=u'Image produit', upload_to='products/images/')
    product = models.ForeignKey('Product', verbose_name=u'Produit associé')

    class Meta:
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImages')

    def __unicode__(self):
        return u', '.join([self.product.name, self.image.url])


class Customer(User):
    profile_picture = models.ImageField(verbose_name=u'Photo de profil', upload_to='customer/images/')

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __unicode__(self):
        return u', '.join([self.username, self.first_name, self.last_name])


class Cart(models.Model):
    OPEN, SUBMITTED = ("Open", "Submitted")

    STATUS_CHOICES = (
        (OPEN, "Open - currently active"),
        (SUBMITTED, "Submitted - has been ordered at the checkout"),
    )
    status = models.CharField(verbose_name=u'Status', max_length=128, default=OPEN, choices=STATUS_CHOICES)
    customer = models.ForeignKey('Customer', verbose_name=u'Client')

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def get_total(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.get_total_line()
        return total

    def __unicode__(self):
        return u' ~ '.join([self.customer.username, self.status, str(self.get_total)])


class CartItem(models.Model):
    product = models.ForeignKey('Product', verbose_name=u'Produit')
    quantity = models.PositiveIntegerField(verbose_name=u'Quantité')
    cart = models.ForeignKey('Cart', verbose_name=u'Panier')

    class Meta:
        verbose_name = _('CartItem')
        verbose_name_plural = _('CartItems')

    def get_total_line(self):
        return self.quantity * self.product.price

    def __unicode__(self):
        return u' ~ '.join([self.product.name, str(self.quantity), str(self.get_total_line)])


class Order(models.Model):
    cart = models.ForeignKey('Cart', verbose_name=u'Panier')
    customer = models.ForeignKey('Customer', verbose_name=u'Client')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return u'Order :' + u' '.join([self.cart.__unicode__(), self.customer.__unicode__()])


class Comment(models.Model):
    product = models.ForeignKey('Product', verbose_name=u'Produit')
    customer = models.ForeignKey('Customer', verbose_name=u'Client')
    text = models.TextField(verbose_name=u'Texte')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __unicode__(self):
        return u' ~ '.join([self.product.name, self.customer.username, self.text])
