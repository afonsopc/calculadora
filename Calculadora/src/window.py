# window.py
#
# Copyright 2022 User
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

import math

def calculate(string):
    string = string.replace(' ', '')
    equacao = []
    numero = ''
    skip = 0

    # Separar numeros dos operadores, fazer contas dentro de parentesis e fazer os sen, cos, tan, sqrt, %, pi e ²
    for idx, item in enumerate(string):
        if skip == 0:
            if item.isnumeric() and item != '²' or item == '.':
                numero += item
            elif item == '(':
                parentesis_fechado_encontrado = False
                parentesis_abertos = 0
                n = idx+1
                while not parentesis_fechado_encontrado:
                    if string[n] == '(':
                        parentesis_abertos += 1
                    elif string[n] == ')':
                        if parentesis_abertos > 0:
                            parentesis_abertos -= 1
                        else:
                            parentesis_fechado_encontrado = True
                            parentesis_fechado = n
                    n += 1
                if string[idx-3:idx] == 'sen':
                    res = calculate(string[idx+1:parentesis_fechado])
                    res = math.radians(res)
                    res = math.sin(res)
                elif string[idx-3:idx] == 'cos':
                    res = calculate(string[idx+1:parentesis_fechado])
                    res = math.radians(res)
                    res = math.cos(res)
                elif string[idx-3:idx] == 'tan':
                    res = calculate(string[idx+1:parentesis_fechado])
                    res = math.radians(res)
                    res = math.tan(res)
                elif string[idx-1:idx] == '√':
                    res = calculate(string[idx+1:parentesis_fechado])
                    res = math.sqrt(res)
                elif string[idx-1:idx] == '%':
                    res = calculate(string[idx+1:parentesis_fechado])
                    res = res/100
                elif string[idx-1:idx] == '^':
                    exp = calculate(string[idx+1:parentesis_fechado])
                    print(float(numero), int(exp))
                    try:
                        res = float(numero)**int(exp)
                    except:
                        res = int(numero)**int(exp)
                    numero = str(res)
                    equacao.append(numero)
                    numero = ''
                else:
                    res = calculate(string[idx+1:parentesis_fechado])
                equacao.append(str(res))
                skip = n-idx-1
            elif item in ['+', '/', '×', '-']:
                equacao.append(numero)
                equacao.append(item)
                numero = ''
            elif item == 'π':
                equacao.append(math.pi)
            if idx == len(string)-1:
                equacao.append(numero)
                numero = ''
        else:
            skip -= 1

    # Remover strings vazias
    while '' in equacao:
        equacao.remove('')

    # Fazer as contas de multiplicação e divisão
    for idx, item in enumerate(equacao):
        if item in ['/', '×']:
            if item == '/':
                resultado = float(equacao[idx-1]) / float(equacao[idx+1])
                equacao[idx+1] = str(resultado)
            elif item == '×':
                resultado = float(equacao[idx-1]) * float(equacao[idx+1])
                equacao[idx+1] = str(resultado)
            equacao[idx] = 'remover'
            equacao[idx-1] = 'remover'

    # Remover 'remover'es da lista causados pelo for anterior
    while 'remover' in equacao:
        equacao.remove('remover')

    # Fazer as multiplicações e as subtrações
    resultado = float(equacao[0])
    for idx, item in enumerate(equacao):
        if item in ['+', '-']:
            if item == '+':
                resultado += float(equacao[idx+1])
            elif item == '-':
                resultado -= float(equacao[idx+1])

    return resultado

@Gtk.Template(resource_path='/org/afonsocoutinho/calculadora/window.ui')
class CalculadoraWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CalculadoraWindow'
    calculator_display = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculator_display.connect("activate", self.on_equals_button)

    def add_to_display_text(self, text):
        cursor_position = self.calculator_display.props.cursor_position
        position = cursor_position + len(text)
        self.calculator_display.insert_text(text, cursor_position)
        self.calculator_display.set_position(position)


    @Gtk.Template.Callback()
    def on_0_button(self, *args):
        self.add_to_display_text('0')

    @Gtk.Template.Callback()
    def on_1_button(self, *args):
        self.add_to_display_text('1')

    @Gtk.Template.Callback()
    def on_2_button(self, *args):
        self.add_to_display_text('2')

    @Gtk.Template.Callback()
    def on_3_button(self, *args):
        self.add_to_display_text('3')

    @Gtk.Template.Callback()
    def on_4_button(self, *args):
        self.add_to_display_text('4')

    @Gtk.Template.Callback()
    def on_5_button(self, *args):
        self.add_to_display_text('5')

    @Gtk.Template.Callback()
    def on_6_button(self, *args):
        self.add_to_display_text('6')

    @Gtk.Template.Callback()
    def on_7_button(self, *args):
        self.add_to_display_text('7')

    @Gtk.Template.Callback()
    def on_8_button(self, *args):
        self.add_to_display_text('8')

    @Gtk.Template.Callback()
    def on_9_button(self, *args):
        self.add_to_display_text('9')

    @Gtk.Template.Callback()
    def on_percentage_button(self, *args):
        self.add_to_display_text('%()')

    @Gtk.Template.Callback()
    def on_parentheses_button(self, *args):
        self.add_to_display_text('()')

    @Gtk.Template.Callback()
    def on_sen_button(self, *args):
        self.add_to_display_text('sen()')

    @Gtk.Template.Callback()
    def on_cos_button(self, *args):
        self.add_to_display_text('cos()')

    @Gtk.Template.Callback()
    def on_tan_button(self, *args):
        self.add_to_display_text('tan()')

    @Gtk.Template.Callback()
    def on_dot_button(self, *args):
        self.add_to_display_text('.')

    @Gtk.Template.Callback()
    def on_plus_button(self, *args):
        self.add_to_display_text('+')

    @Gtk.Template.Callback()
    def on_minus_button(self, *args):
        self.add_to_display_text('-')

    @Gtk.Template.Callback()
    def on_division_button(self, *args):
        self.add_to_display_text('÷')

    @Gtk.Template.Callback()
    def on_squared_button(self, *args):
        self.add_to_display_text('√()')

    @Gtk.Template.Callback()
    def on_exponent_button(self, *args):
        self.add_to_display_text('^()')

    @Gtk.Template.Callback()
    def on_multiply_button(self, *args):
        self.add_to_display_text('×')

    @Gtk.Template.Callback()
    def on_pi_button(self, *args):
        self.add_to_display_text('π')

    @Gtk.Template.Callback()
    def on_clear_button(self, *args):
        self.calculator_display.set_text('')

    @Gtk.Template.Callback()
    def on_equals_button(self, *args):
        invalid_txt = 'Inválido'
        raw = self.calculator_display.get_text()
        raw = str(raw)
        try:
            res = calculate(raw)
        except Exception as e:
            print(e)
            res = invalid_txt
        res = str(res)
        self.calculator_display.set_text(res)


