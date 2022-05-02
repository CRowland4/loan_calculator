import argparse
import math


parser = argparse.ArgumentParser()

parser.add_argument('--type')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')
parser.add_argument('--payment')

args = parser.parse_args()


def calc_nominal_interest(interest_rate):
    l_nominal = float(interest_rate / (12 * 100))
    return l_nominal


def validate_parameters(l_args):
    parameters = [args.type, args.principal, args.periods, args.interest, args.payment]

    if any([
        l_args.type not in ['annuity', 'diff'],
        l_args.type == 'diff' and l_args.payment,
        not l_args.interest,
        parameters.count(None) >= 2,
        any([float(number) < 0 for number in parameters[1:] if number])
    ]):
        return "Incorrect parameters"
    else:
        return False


def calc_diff_payments(p, n, i):
    interest = calc_nominal_interest(i)
    diff_payments = []

    for m in range(1, n + 1):
        payment = math.ceil((p / n) + interest * (p - ((p * (m - 1)) / n)))
        print(f'Month {m}: payment is {payment}')
        diff_payments.append(payment)

    overpayment = sum(diff_payments) - p
    print(f"Overpayment = {overpayment}")


def calc_principal(a, n, i):
    interest = calc_nominal_interest(i)
    l_principal = (a * (((1 + interest) ** n) - 1)) / (interest * ((1 + interest) ** n))
    print(f'Your loan principal = {l_principal}!')


def calc_payment_number(p, a, i):
    interest = calc_nominal_interest(i)
    l_payments = math.log(a / (a - interest * p), 1 + interest)
    return l_payments


def calc_loan_time(p, a, i):
    periods = math.ceil(calc_payment_number(p, a, i))
    if periods == 1:
        print(f'It will take {periods} month to repay this loan!')
    elif periods < 12:
        print(f'It will take {periods} months to repay this loan!')
    elif periods == 12:
        print(f'It will take {periods} year to repay this loan!')
    elif periods == 13:
        print('It will take 1 year and 1 month to repay this loan!')
    elif periods < 24:
        print(f'It will take 1 year and {periods} months to repay this loan!')
    elif periods % 12 == 0:
        print(f'It will take {int(periods / 12)} years to repay this loan!')
    elif periods % 12 == 1:
        print(f'It will take {int(periods // 12)} years and 1 month to repay this loan!')
    else:
        years = periods // 12
        months = periods % 12
        print(f'It will take {years} years and {months} months to repay this loan!')

    overpayment = (periods * a) - p
    print(f'Overpayment = {overpayment}')


def calc_annuity_payments(p, n, i):
    interest = calc_nominal_interest(i)
    l_annuity = math.ceil(p * ((interest * ((1 + interest) ** n)) / (((1 + interest) ** n) - 1)))
    overpayment = (n * l_annuity) - p
    print(f"""Your monthly payment = {l_annuity}!
    Overpayment = {overpayment}""")


def give_answer():
    global args
    if args.type == 'diff':
        calc_diff_payments(float(args.principal), int(args.periods), float(args.interest))
    elif args.type == 'annuity':
        if not args.payment:
            calc_annuity_payments(float(args.principal), int(args.periods), float(args.interest))
        elif not args.principal:
            calc_principal(float(args.payment), int(args.periods), float(args.interest))
        elif not args.periods:
            calc_loan_time(int(args.principal), int(args.payment), float(args.interest))


print(validate_parameters(args) or give_answer())
