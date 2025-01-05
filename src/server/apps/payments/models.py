# from django.db import models
#
# from server.apps.accounts.models import Account
#
#
# class Payments(models.Model):
#     """Модель истории транзакций из лк банка"""
#
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Транзакция'
#         verbose_name_plural = 'Транзакции'
#         ordering = ['id']
#
#     def __str__(self):
#         return str(self.account.title)
