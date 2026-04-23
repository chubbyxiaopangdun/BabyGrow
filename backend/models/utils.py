"""
共享工具函数
"""
from datetime import date


def calc_age_months(birth_date: date) -> int:
    """计算月龄"""
    today = date.today()
    months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    if today.day < birth_date.day:
        months -= 1
    return max(0, months)


def calc_age_display(age_months: int) -> str:
    """计算月龄显示"""
    if age_months < 12:
        return f"{age_months}个月"
    years = age_months // 12
    months = age_months % 12
    if months == 0:
        return f"{years}岁"
    return f"{years}岁{months}个月"
