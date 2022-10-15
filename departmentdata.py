_AITR_DEPTS = [ 
    (r'Combined', 'CO'),
    (r'B. Sc (CS)',       'ATBS'),
    (r'B. Tech (CSE)',    'ATCS'),
    (r'B. Tech (IT)',     'ATIT'),
    (r'B. Tech (AIML',    'ATAI'),
    (r'B. Tech (ECE)',    'ATEC'),
    (r'B. Tech (CE)',     'ATCE'),
    (r'B. Tech (ME)',     'ATME'),
    (r'B. Tech (CSIT)',   'ATCI'),
    (r'M. Tech',          'ATMT'),
    (r'Diploma',          'ATDP'),
]

_AIMSR_DEPTS = [
    (r'Combined', 'CO'),
    (r'BBA',                     'AMBB'),
    (r'B.Com',                   'AMBC'),
    (r'B. Sc. (Biotechnology)',  'AMBS'),
    (r'M.Sc. Biotechnology',     'AMMS'),
    (r'B.A.',                    'AMBA'),
]

_AIPER_DEPTS = [
    (r'Combined', 'CO'),
    (r'B. Pharma', 'APBP'),
    (r'D. Pharma.', 'APDP'),
]

_AFMR_DEPTS = [
    (r'Combined', 'CO'),
    (r'MBA', 'AFMB'),
]

_FCA_DEPTS = [
    (r'Combined', 'CO'),
    (r'BCA', 'ACBC'),
    (r'MCA', 'ACMC'),
    (r'DDMCA', 'ACDC'),
    (r'IMCA', 'ACIM'),
]

_AIL_DEPTS = [
    (r'Combined', 'CO'),
    (r'BA LLB', 'ALBA'),
    (r'BBA LLB', 'ALBB'),
]

_AID_DEPTS = [
    (r'Combined', 'CO'),
    (r'B. Design', 'ADBD'),
]

_ALL_DEPTS = [
    ('Combined', 'CO'),
]

_DEPARTMENTSCODE = (
    _AITR_DEPTS, 
    _AIMSR_DEPTS,
    _AIPER_DEPTS,
    _AFMR_DEPTS,
    _FCA_DEPTS,
    _AIL_DEPTS,
    _AID_DEPTS,
    _ALL_DEPTS,
)

institutes  = (
    'AITR', 'AIMSR', 
    'AIPER', 'AFMR', 
    'FCA', 'AIL', 
    'AID', 'Mixed'
)

departments = []
for deptandcodelist in _DEPARTMENTSCODE:
    departments.append([dept for dept, code in deptandcodelist])

INST_DEPT_MAP = dict(zip( institutes, departments ))
DEPT_CODE_MAP = dict(sum(_DEPARTMENTSCODE, []))

# DEPT_CODE_MAP = dict(temp.extend(l) for l in _DEPARTMENTSCODE)
# DEPT_CODE_MAP = dict(l for l in _DEPARTMENTSCODE)

if __name__ == '__main__':
    from pprint import pprint
    pprint(INST_DEPT_MAP)
    pprint(DEPT_CODE_MAP)