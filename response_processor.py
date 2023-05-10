import jellyfish
import sympy
from sympy.solvers import solve
from kb import DATA
import numpy as np
import matplotlib.pyplot as plt

IGNORED_QUERY_TOKENS = [',', '.', '!', '?']
QUERY_SIMILARITY_THRESHOLD = 0.7


def get_degree_of_similarity(str1: str, str2: str) -> float:
    return jellyfish.jaro_distance(str1, str2)


def get_max_degree_of_similarity(query: str, preset_queries) -> float:
    similarity_degrees = []
    for preset_def_query in preset_queries:
        similarity_degrees.append(get_degree_of_similarity(query, preset_def_query))
    return max(similarity_degrees)


def get_most_similar(string: str, preset_strings) -> str:
    most_similar_string = ''
    most_similar_string_similarity = 0
    for preset_string in preset_strings:
        similarity = get_degree_of_similarity(string, preset_string)
        if (similarity > most_similar_string_similarity):
            most_similar_string_similarity = similarity
            most_similar_string = preset_string
    return most_similar_string


####################################
####################################
####################################

PRESET_DEFINITION_QUERIES = [
    'что такое',
    'расскажи о',
    'расскажи о том что такое',
    'дай определение',
    'как можно определить',
    'что значит',
    'что означает',
    'что значит термин',
    'что означает термин',
    'какой смысл имеет термин'
]


def is_definition_query(query: str) -> bool:
    return get_max_degree_of_similarity(query, PRESET_DEFINITION_QUERIES) > QUERY_SIMILARITY_THRESHOLD


####################################
####################################
####################################

PRESET_SOLUTION_QUERIES = [
    'реши уравнение',
    'найди корни уравнения',
    'каковы решения уравнения',
    'найди корни',
    'реши',
    'вычисли корни',
    'вычисли корни уравнения'
]


def is_solution_query(query: str) -> bool:
    return get_max_degree_of_similarity(query, PRESET_SOLUTION_QUERIES) > QUERY_SIMILARITY_THRESHOLD


PRESET_GRAPHIC_QUERIES = [
    'построй график',
    'построй график функции',
    'нарисуй график',
    'нарисуй график функции',
    'график',
    'гистограмма',
    'построй гистограмму',
    'нарисуй гистограмму'
]


def is_graphic_query(query: str) -> bool:
    return get_max_degree_of_similarity(query, PRESET_GRAPHIC_QUERIES) > QUERY_SIMILARITY_THRESHOLD


PRESET_SIMP_QUERIES = [
    'упростить',
    'упростить выражение',
    'упрости',
    'упрости выражение'
]


def is_simp_query(query: str) -> bool:
    return get_max_degree_of_similarity(query, PRESET_SIMP_QUERIES) > QUERY_SIMILARITY_THRESHOLD


def strip_spaces(string: str) -> str:
    return ''.join(string.split(' '))


def transform_equation_to_uniform_and_return_LHS(equation: str) -> str:
    index_of_eq_sign = equation.index('=')
    before_eq = equation[:index_of_eq_sign]
    after_eq = equation[index_of_eq_sign + 1:]

    after_eq_negated = f'-({after_eq})'
    before_eq = f'{before_eq}{after_eq_negated}'
    return before_eq


numpy_functions = ['log', 'log2', 'log10', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'abs', 'exp', 'sqrt']


def form_function_for_graphic(equation: str) -> str:
    if '=' in equation:
        index_of_eq_sign = equation.index('=')
        after_eq = equation[index_of_eq_sign + 1:]
    else:
        after_eq = equation
    for func in numpy_functions:
        after_eq = after_eq.replace(func, f"np.{func}")
    for sym in after_eq:
        if sym == '^':
            after_eq = after_eq.replace(sym, '**')
    return after_eq


def form_function_for_simp(equation: str) -> str:
    if '=' in equation:
        index_of_eq_sign = equation.index('=')
        after_eq = equation[index_of_eq_sign + 1:]
    else:
        after_eq = equation
    for sym in after_eq:
        if sym == '^':
            after_eq = after_eq.replace(sym, '**')
    return after_eq



####################################
####################################
####################################

def strip_useless_tokens(query: str) -> str:
    for token in IGNORED_QUERY_TOKENS:
        query = query.replace(token, '')
    return query


def response(query: str) -> str:
    query = strip_useless_tokens(query).lower()

    if is_definition_query(query):
        REQUIRED_DEF = query.split()[-1]
        DEFS = DATA['definitions']
        return DEFS[get_most_similar(REQUIRED_DEF, list(DEFS.keys()))]

    elif is_solution_query(query):
        # pre_equation_query = get_most_similar(query, PRESET_SOLUTION_QUERIES)
        equation = query.split(" ")[-1]
        equation = strip_spaces(equation)
        equation = transform_equation_to_uniform_and_return_LHS(equation)
        solutions = solve(equation)
        if (len(solutions) == 0):
            return 'У этого уравнения нет корней.'
        return f'Решение(я) уравнения: {", ".join(str(s) for s in solutions)}.'
    elif is_graphic_query(query):
        # pre_equation_query = get_most_similar(query, PRESET_GRAPHIC_QUERIES)
        equation = query.split(" ")[-1]
        equation = strip_spaces(equation)
        equation = form_function_for_graphic(equation)
        x = np.arange(-10, 10, 0.1)
        y = eval(equation)
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График функции')
        plt.grid(True)
        path = f"img/{hash(equation)}.png"
        plt.savefig(path)
        plt.clf()
        return path
    elif is_simp_query(query):
        # pre_equation_query = get_most_similar(query, PRESET_SIMP_QUERIES)
        equation = query.split(" ")[-1]
        equation = strip_spaces(equation)
        equation = form_function_for_simp(equation)
        expr = sympy.sympify(equation)
        simplified = str(sympy.simplify(expr))
        simplified = simplified.replace("**", '^')
        return simplified

    else:
        return 'Извините, не понял Вашего запроса. Переформулируйте, пожалуйста.'


# print(response('упрости (x**2 + x**3) * (x**4 + x**5)'))
# print(response('нарисуй график y=sin(x)+abs(x)+2*sin(x)'))
