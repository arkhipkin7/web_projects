import numpy as np

from typing import Dict

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models.functions import Upper, Substr
from django_filters.views import FilterView
from django_filters.views import FilterMixinRenames

from .models import Employee
from .filters import EmployeeFilter

NUMBER_OF_GROUP = 7


class EmployeesView(FilterView):
    filterset_class = EmployeeFilter
    template_name = 'catalog/employees.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_filterset(self, filterset_class) -> FilterMixinRenames:
        r = self.request.GET
        if r:
            self.request.session['filter'] = r
        else:
            r = self.request.session.get('filter', self.request.GET)
        return filterset_class(r, queryset=Employee.objects.all())


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'catalog/employee_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Employee, pk=self.kwargs.get('pk'))


class EmployeesAlphabetView(ListView):
    model = Employee
    template_name = 'catalog/employees_alphabet.html'
    context_object_name = 'employees'

    @staticmethod
    def get_letter() -> Dict:
        all_letters = list(
            [upper_latter['letter'] for upper_latter in
             Employee.objects.annotate(letter=Upper(Substr('last_name', 1, 1))).values('letter')])

        get_groups = [
            all_letters[i * len(all_letters) // NUMBER_OF_GROUP: (i + 1) * len(all_letters) // NUMBER_OF_GROUP]
            for i in np.arange(NUMBER_OF_GROUP)]

        for i in np.arange(len(get_groups) - 1):
            try:
                last_latter_1 = get_groups[i][-1]
                first_latter_2 = get_groups[i + 1][0]
                if last_latter_1 == first_latter_2:
                    latter = last_latter_1
                    count_1 = [w for w in get_groups[i] if w == latter]
                    count_2 = [w for w in get_groups[i + 1] if w == latter]
                    if len(count_1) >= len(count_2):
                        get_groups[i] = get_groups[i] + count_2
                        get_groups[i + 1] = [w for w in get_groups[i + 1] if w != latter]
                    elif len(count_1) < len(count_2):
                        get_groups[i + 1] = count_1 + get_groups[i + 1]
                        get_groups[i] = [w for w in get_groups[i] if w != latter]
            except:
                pass

        letters_in_group = {id_group: letter[0] + '-' + letter[-1] for id_group, letter in enumerate(get_groups) if
                            letter}

        return {'get_groups': get_groups, 'letters_in_group': letters_in_group}

    def get_queryset(self):
        try:
            return Employee.objects.annotate(letter=Upper(Substr('last_name', 1, 1))).filter(
                letter__in=self.get_letter()['get_groups'][int(self.request.GET['group'])])
        except KeyError:
            return Employee.objects.annotate(letter=Upper(Substr('last_name', 1, 1))).filter(
                letter__in=self.get_letter()['get_groups'][0])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeesAlphabetView, self).get_context_data(**kwargs)
        context['letters_in_group'] = self.get_letter()['letters_in_group']
        return context
