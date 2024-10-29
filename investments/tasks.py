from investments.utils import get_selic_rate
from .models import Indexer, Investment
from celery import shared_task
from datetime import date


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_income(self):
    investments = Investment.objects.filter(status="ativo")
    try:
        for investment in investments:
            investment.update_income()
            investment.save()
            print(
                f"Investimento de {investment.account} atualizado com sucesso!"
                )
    except Exception as exc:
        raise self.retry(exc=exc)
    return "Atualização concluída com sucesso!"

@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def update_selic(self):
    selic_indexer, _ = Indexer.objects.get_or_create(name="SELIC", rate=0)
    try:
        selic_rate = get_selic_rate()
        if not selic_rate:
            raise Exception("Não foi possível obter a taxa SELIC")
        selic_indexer.rate = selic_rate
        selic_indexer.save()
    except Exception as exc:
        raise self.retry(exc=exc)
    return f"Indexador SELIC atualizado: {selic_indexer.rate}"

@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def finalize_investments(self):
    expired_investments = Investment.objects.filter(
        due_date__lt=date.today(),
        status="ativo"
        )
    try:
        for investment in expired_investments:
            investment.status = "vencido"
            investment.rescue_data = date.today()
            investment.account.balance += (
                investment.accumulated_income + investment.applied_value
                )
            investment.account.save()
            investment.save()
            print(
                f"""Investimento de {
                    investment.account
                    } vencido, valor resgatado: {
                        (
                            investment.accumulated_income +
                            investment.applied_value
                        )
                        }!"""
            )
    except Exception as exc:
        raise self.retry(exc=exc)
    return "Investimentos expirados resgatados"
