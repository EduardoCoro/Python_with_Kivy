from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from datetime import datetime
import math
#from kivy.uix.card import Card
#from kivy.garden.iconfonts import *
from os.path import join, dirname
import sqlite3 as sql
import json

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)

    def confirmacao(self, *args, **kwargs):
        self.export_to_png('Menu.png')
        print('Chamou')
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='Deseja mesmo sair?', content=box, size_hint=(None, None),
                    size=(150, 150))

        sim = Botao_confirma(text='Sim', on_release=App.get_running_app().stop)
        nao = Botao_cancelar(text='Não', on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='image/atencao.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        animText = Animation(color=(0, 0, 0, 1)) + Animation(color=(1, 1, 1, 1))
        animText.repeat = True
        animText.start(sim)
        anim = Animation(size=(300, 180), duration=0.2, t='out_back')
        anim.start(pop)
        pop.open()
        return True





class resultados(Screen):

    def on_pre_enter(self):
        con = sql.connect('user.db')

        cur = con.cursor()

        cur.execute("""
                                    SELECT * FROM TESTE;
                                    """)

        # cur.execute(""" SELECT idade FROM TESTE where id = 1 """)

        for linha in cur.fetchall():
            altura = linha[4] / ((linha[5] * linha[5]) / 10000)
            sexo=linha[3]
            p=linha[4]
            al=linha[5]
            id=linha[2]
            #self.ids.r_imc.text=str(self.imc(linha[5],linha[4]))
            #self.ids.idade_texto.text = str(linha[2])
            #self.ids.peso_texto.text = str(linha[4])
            #self.ids.altura_texto.text = str(linha[5])

            #if linha[3] == 'm':
             #   self.ids.chk_m.active = True
            #else:
             #   self.ids.chk_f.active = True




        if altura >= 18.5 and altura <= 24.9:
            peso = "Normal"

        elif altura >= 25 and altura <= 29.9:
            peso = "Sobrepeso"

        elif altura >= 30 and altura <= 39.9:
            peso = "Obesidade"
        elif altura >= 40:
            peso = "Obesidade Grave"
        else:
            peso = "Magreza"

        #mostrar resultado
        texto= " "+ str(peso) +" de :"+ str(altura)
        self.ids.r_imc.text = str(texto)

        # calcular tmb
        if sexo == 'm':
            cal = 66 + (13.7 * p) + (5 * al) - (6.8 * id)


        elif sexo == 'f':
            cal = 655 + (9.6 * p) + (1.7 * al) - (4.7 * id)

        else:
            print("erro_sem dados")

        #mostrar resultado de tmb
        texto = " "+str(cal)
        self.ids.r_tbm.text= str(texto)
        cur.close()


class perfil(Screen):





    def on_pre_enter(self):

        #btn = Botao_confirma(id='ok_btn', font_size='18', text='Gravar', color='0, 0, 0, 1', on_release='')
        #box = self.ids.bx_btn
       # box.add_widget(btn)
        con = sql.connect('user.db')


        cur = con.cursor()

        cur.execute("""
                            SELECT * FROM TESTE;
                            """)

       # cur.execute(""" SELECT idade FROM TESTE where id = 1 """)


        for linha in cur.fetchall():
                 self.ids.idade_texto.text = str(linha[2])
                 self.ids.peso_texto.text = str(linha[4])
                 self.ids.altura_texto.text = str(linha[5])
                 if linha[3] == 'm':
                     self.ids.chk_m.active=True
                 else:
                     self.ids.chk_f.active=True



               #  if linha[1] =='' or linha[5]=='':
                #      btn = self.id.ok_btn(on_release=self.atualizar())
               #  else:
               #        self.id.ok_btn(on_release=self.atualizar())

        cur.close()




    def atualizar(self):
        nome = "usuario"

        if self.ids.chk_m.active == True:
              sexo= 'm'

        elif self.ids.chk_f.active == True:
              sexo='f'

        con = sql.connect('user.db')

        cur = con.cursor()



        # alterando os dados da tabela
        cur.execute("""
        UPDATE TESTE
        SET nome = ?, idade = ?, sexo = ?, peso= ?, altura=?
        WHERE id = 1
        """, (nome, int(self.ids.idade_texto.text),sexo, float(self.ids.peso_texto.text) ,int(self.ids.altura_texto.text)))



        # consultando os dados e exibindo no terminal
        cur.execute("""
                                SELECT * FROM TESTE;
                                """)

        for linha in cur.fetchall():
            print(linha)


        con.commit()
        cur.close()



    def consultar(self):

        con = sql.connect('user.db')

        cur = con.cursor()

        cur.execute("""
                SELECT * FROM TESTE;
                """)

        abc = cur.execute("""
                SELECT * FROM TESTE;
                """)

        #print(abc)
        for linha in cur.fetchall():
            print(linha)

        cur.close()

    def inserir(self):
        nome = "usuario"
        #id = 1
        #idade= int(self.ids.idade_texto.text)
        #altura = int(self.ids.altura_texto.text)
        #peso = float(self.ids.peso_texto.text)

        if self.ids.chk_m.active == True:
              sexo= 'm'

        elif self.ids.chk_f.active == True:
              sexo='f'


        con = sql.connect('user.db')

        cur = con.cursor()

        cur.execute(""" INSERT INTO TESTE( nome, idade, sexo, peso, altura) VALUES (?,?,?,?,?)""", (nome, int(self.ids.idade_texto.text),sexo, float(self.ids.peso_texto.text) ,int(self.ids.altura_texto.text))

                    )

        con.commit()

        # lendo os dados
        cur.execute("""
        SELECT * FROM TESTE;
        """)

        for linha in cur.fetchall():
            print(linha)

        #rs = cur.dictfetchall()
        #print(rs[0])

        con.close()


#botao personalizado
class Botao_cancelar(ButtonBehavior,Label):
      pass

class Botao_confirma(ButtonBehavior,Label):
      pass

#botao menu
class Botao(ButtonBehavior,Label):
    cor = ListProperty([0.1, 0.5, 0.7, 1])
    cor2 = ListProperty([0.1, 0.1, 0.1, 1])

    def __init__(self,**kwargs):
        super(Botao,self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self,*args):
        self.atualizar()

    def on_size(self,*args):
        self.atualizar()

    def on_press(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_release(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_cor(self,*args):
        self.atualizar()

    def atualizar(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),
                    pos=self.pos)
            Ellipse(size=(self.height,self.height),
                    pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),
                      pos=(self.x+self.height/2.0,self.y))





class Tarefas(Screen):
    tarefas = []
    path = ''

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.path = App.get_running_app().user_data_dir+'/'
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'calculo'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:
            with open(self.path+'data.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self,*args):
        with open(self.path+'data.json','w') as data:
            json.dump(self.tarefas,data)

    def removeWidget(self,tarefa):
        
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self):
        
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()

class Tarefa(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Tarefa,self).__init__(**kwargs)
        self.ids.label.text = text

#class Resultado_IMC(BoxLayout):
 #   def __init__(self,text='',**kwargs):
  #      super(Resultado_IMC,self).__init__(**kwargs)
   #     self.ids.valor.text = text

class Calculo(Screen):
    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

class ImageButton(ButtonBehavior, Image):
    pass


 

class IMC(Screen):
    
    altura = 0
    peso = ""
    
    tarefas = []
    path = ''

    def on_pre_enter(self):
        #self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        #for tarefa in self.tarefas:
          #  self.ids.box.add_widget(Historicos(text=tarefa))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'calculo'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:
            with open(self.path+'data_imc.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self,*args):
        with open(self.path+'data_imc.json','w') as data:
            json.dump(self.tarefas,data)


    
    


    def calcular(self):
       
       
         
 
       altura = float(self.ids.peso_texto.text) / ((float(self.ids.altura_texto.text) * float(self.ids.altura_texto.text))/10000)
       
       if altura >= 18.5  and altura <=24.9 :
           peso ="Normal"
           
       elif altura >= 25  and altura <=29.9:
           peso ="Sobrepeso" 
             
       elif altura >= 30  and altura <=39.9:
           peso ="Obesidade"
       elif altura >= 40:
           peso ="Obesidade Grave"
       else:
           peso ="Magreza"

       #now = datetime.now()
       self.tarefas.append('- Nivel: '+ peso + ' - Valor: ' +str(round(altura,3)))
       print(self.tarefas)
       #self.tarefas.append(str(truncate(altura)))
       self.saveData()
       #{altura:.2f}
       
       #texto = self.ids.texto.text
       #self.ids.box.add_widget(Resultado_IMC(text=t))
       
       self.ids.valor.text="IMC - " + peso
       self.ids.nt_valor.text ="" + str(altura)
       

    def limpar(self):
      self.ids.nt_valor.text=""
      self.ids.peso_texto.text=""
      self.ids.altura_texto.text=""
      #self.ids.peso_texto.focus()



class TAXACALORICA(Screen):
  
  tarefas = []
  path = ''

  def on_pre_enter(self):
        #self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        #for tarefa in self.tarefas:
          #  self.ids.box.add_widget(Historicos(text=tarefa))

  def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'calculo'
            return True

  def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

  def loadData(self,*args):
        try:
            with open(self.path+'data_tx_atv.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

  def saveData(self,*args):
        with open(self.path+'data_tx_atv.json','w') as data:
            json.dump(self.tarefas,data)


  def calcular(self):

    if self.ids.chk_corrida.active==True:
               gasto = float(self.ids.temp_atv.text) * 16
               self.tarefas.append('Corrida - Gasto: '+ str(gasto))
    elif self.ids.chk_caminhada.active==True:
          gasto = float(self.ids.temp_atv.text) * 6.1
          self.tarefas.append('Caminhada - Gasto: '+ str(gasto))
    elif self.ids.chk_natacao.active==True:
            gasto = float(self.ids.temp_atv.text) *  9.8
            self.tarefas.append('Natacao - Gasto: '+ str(gasto))
    elif self.ids.chk_ciclismo.active==True:
             gasto = float(self.ids.temp_atv.text) * 4.9
             self.tarefas.append('Ciclismo - Gasto: '+ str(gasto))
    else:
       print("erro_sem dados")
     

    self.ids.valor.text="Gasto calorico- " + str(gasto)
    #self.tarefas.append('Gasto: '+ str(gasto))
    print(self.tarefas)
    self.saveData()

  def limpar(self):
      self.ids.temp_atv.text=""
      self.ids.valor.text=""
      self.ids.chk_corrida.text=""
      self.ids.chk_caminhada.active==False
      self.ids.chk_natacao.active==False
      self.ids.chk_ciclismo.active==False


class CALCULADORA(Screen):
     
    class CalcGridLayout(GridLayout):
    # Function called when equals is pressed
           def calculate(self, calculation):
             if calculation:
                try:
                # Solve formula and display it in entry
                # which is pointed at by display
                   self.display.text = str(eval(calculation))
                except Exception:
                   self.display.text = "Error"

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'calculo'
            return True


class TMB(Screen):

  #calculo=0
  #altura = 0
  #peso = ""
    
  tarefas = []
  path = ''

  def on_pre_enter(self):
        #self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        #for tarefa in self.tarefas:
          #  self.ids.box.add_widget(Historicos(text=tarefa))

  def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'calculo'
            return True

  def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

  def loadData(self,*args):
        try:
            with open(self.path+'data_tmb.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

  def saveData(self,*args):
        with open(self.path+'data_tmb.json','w') as data:
            json.dump(self.tarefas,data)

  def calcular(self):
     calculo=0
    #try:
       #modo = self.ids.sexo_txt.text
     if self.ids.chk_m.active == True:
           calculo = 66 + (13.7 * float(self.ids.peso_txt.text)) + (5 * float(self.ids.altura.text)) - (6.8 * float(self.ids.idade.text))
           self.ids.valor.text="Seu TMB - " + str(calculo)
           self.tarefas.append('Masculino P:'+self.ids.peso_txt.text  + ',A-' + self.ids.altura.text +'-TMB:'+ str(calculo))
           print(self.tarefas)
       
           self.saveData()

     elif self.ids.chk_f.active == True:
           calculo = 655 + (9.6 * float(self.ids.peso_txt.text)) + (1.7 * float(self.ids.altura.text)) - (4.7 * float(self.ids.idade.text))
           self.ids.valor.text="Seu TMB - " + str(calculo)
           self.ids.valor.text="Seu TMB - " + str(calculo)
           self.tarefas.append('Feminino P:'+self.ids.peso_txt.text  + ',A-'+ self.ids.altura.text +'-TMB:'+ str(calculo))
           print(self.tarefas)
       
           self.saveData()
     else:
           print("erro_sem dados")
           self.ids.valor.text="Error - Preencha todo os campos"

       
     #now = datetime.now()
     #self.tarefas.append(' TMB: '+ str(calculo))
     #print(self.tarefas)
       
     #self.saveData()
       
      

    #except Exception:
      #        self.ids.valor.text="Preencha os campos"


  def limpar(self):
      self.ids.peso_txt.text=""
      self.ids.valor.text=""
      self.ids.altura.text=""
      self.ids.idade.text=""
      self.ids.chk_m.active==False      
      self.ids.chk_f.active==False

class historico_atv(Screen):
    tarefas = []
    path = ''

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Historicos_taxa(text=tarefa))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'taxacalorica'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:
            with open(self.path+'data_tx_atv.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self,*args):
        with open(self.path+'data_tx_atv.json','w') as data:
            json.dump(self.tarefas,data)

    def removeWidget(self,tarefa):
        
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self):
        
        texto = self.ids.texto.text
        self.ids.box.add_widget(Historicos_taxa(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()

class historico_tmb(Screen):
    tarefas = []
    path = ''

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Historicos_tmb(text=tarefa))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'tmb'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:
            with open(self.path+'data_tmb.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self,*args):
        with open(self.path+'data_tmb.json','w') as data:
            json.dump(self.tarefas,data)

    def removeWidget(self,tarefa):
        
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self):
        
        texto = self.ids.texto.text
        self.ids.box.add_widget(Historicos_tmb(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()


class historico_imc(Screen):
    tarefas = []
    path = ''

    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.path = ''
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Historicos(text=tarefa))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'imc'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:
            with open(self.path+'data_imc.json','r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self,*args):
        with open(self.path+'data_imc.json','w') as data:
            json.dump(self.tarefas,data)

    def removeWidget(self,tarefa):
        
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self):
        
        texto = self.ids.texto.text
        self.ids.box.add_widget(Historicos(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()

class Historicos(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Historicos,self).__init__(**kwargs)
        self.ids.label.text = text

class Historicos_tmb(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Historicos_tmb,self).__init__(**kwargs)
        self.ids.label.text = text

class Historicos_taxa(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Historicos_taxa,self).__init__(**kwargs)
        self.ids.label.text = text

class Test(App):

    def build(self):
        bbt = perfil()
        return Gerenciador()

    try:

        con = sql.connect('user.db')

        cur = con.cursor()

        cur.execute(""" create table TESTE (
                    id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(40) NOT NULL,
                    idade INTEGER NOT NULL,
                    sexo VARCHAR(1) NOT NULL,
                    peso FLOAT(7,4) NOT NULL,
                    altura INTEGER NOT NULL)

                """)

        con.commit()

        con.close()

    except:

        pass




Test().run()
