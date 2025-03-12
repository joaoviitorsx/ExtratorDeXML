import xmltodict
# print(xmltodict)
import os
import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QFileDialog, QMessageBox
import pandas as pd
from utils.mensagem import mensagem_aviso, mensagem_sucesso, mensagem_error
from utils.icone import usar_icone

sucesso = 0
falha = 0
total_arquivos = 0
valor_total = 0


def pegar_infos(nome_arquivo, valores, progresso, lista_arquivos, valores_erros):
    global sucesso, falha, total_arquivos, valor_total
    print("PEGOU AS INFORMAÇÕES DO arquivo", nome_arquivo)
    with open(nome_arquivo, "rb") as arquivo_xml:
        dic_arquivo = xmltodict.parse(arquivo_xml)
        total_arquivos += 1
        print(f"Total de arquivos: {total_arquivos}")
        valor_processado = total_arquivos / len(lista_arquivos) * 100
        print(f"Progresso atual (%): {valor_processado:.2f}")
        progresso.setValue(valor_processado)

        if 'nfeProc' not in dic_arquivo:
            falha += 1
            valores_erros.append(nome_arquivo)
            return

        if 'nfeProc' in dic_arquivo:
            sucesso += 1
            infos_nf = dic_arquivo['nfeProc']['NFe']['infNFe']
            chave_nf = infos_nf['@Id']
            fornecedor = infos_nf['emit'].get('xNome', 'Não informado')
            cnpj_fornecedor = infos_nf['emit'].get('CNPJ', 'Não informado')
            inscricao_estadual = infos_nf['emit'].get('IE', 'Não informado')
            numero_nota = infos_nf['ide'].get('nNF', 'Não informado')
            serie = infos_nf['ide'].get('serie', 'Não informado')
            data_emissao = infos_nf['ide'].get('dhEmi', 'Não informado')
            data_emissao = data_emissao.split('T')[0]
            data_emissao = data_emissao.replace('-', '/')
            data_sai_ent = infos_nf['ide'].get('dhSaiEnt', 'Não informado')
            data_sai_ent = data_sai_ent.split('T')[0]
            data_sai_ent = data_sai_ent.replace('-', '/')
            

            nome_cliente = infos_nf['dest'].get('xNome', 'Não informado')
            cnpj_cliente = infos_nf['dest'].get('CNPJ', 'Não informado')
            nome_do_arquivo = nome_arquivo.split('/')[-1]
            nome_do_arquivo = nome_do_arquivo.split("\\")[-1]

            produtos = infos_nf['det']

            if not isinstance(produtos, list):
                produtos = [produtos]

        try:

            for produto in produtos:
                try:
                    numero_item = produto['nItem']
                except:
                    numero_item = produto['@nItem']
                cod_produto = produto['prod'].get('cProd', 'Não informado')
                ean = produto['prod'].get('cEAN', 'Não informado')
                nome_produto = produto['prod'].get('xProd', 'Não informado')
                ncm = produto['prod'].get('NCM', 'Não informado')
                cfop = produto['prod'].get('CFOP', 'Não informado')
                quantidade = produto['prod'].get('qCom', 'Não informado')
                if quantidade != 'Não informado':
                    quantidade = quantidade.replace('.', ',')
                valor_unitario = produto['prod'].get('vUnCom', 'Não informado')
                if valor_unitario != 'Não informado':
                    valor_unitario = valor_unitario.replace('.', ',')
                valor_frete = produto['prod'].get('vFrete', 'Não informado')
                if valor_frete != 'Não informado':
                    valor_frete = valor_frete.replace('.', ',')
                valor_seguro = produto['prod'].get('vSeg', 'Não informado')
                if valor_seguro != 'Não informado':
                    valor_seguro = valor_seguro.replace('.', ',')
                valor_desconto = produto['prod'].get('vDesc', 'Não informado')
                if valor_desconto != 'Não informado':
                    valor_desconto = valor_desconto.replace('.', ',')
                valor_outros = produto['prod'].get('vOutro', 'Não informado')
                if valor_outros != 'Não informado':
                    valor_outros = valor_outros.replace('.', ',')
                valor_produto = produto['prod'].get('vProd', 'Não informado')
                if valor_produto != 'Não informado':
                    valor_produto = valor_produto.replace('.', ',')
                ean_tributado = produto['prod'].get('cEANTrib', 'Não informado')
                unidade_tributada = produto['prod'].get('uTrib', 'Não informado')
                quantidade_tributada = produto['prod'].get('qTrib', 'Não informado')
                if quantidade_tributada != 'Não informado':
                    quantidade_tributada = quantidade_tributada.replace('.', ',')
                valor_unitario_tributado = produto['prod'].get('vUnTrib', 'Não informado')
                if valor_unitario_tributado != 'Não informado':
                    valor_unitario_tributado = valor_unitario_tributado.replace('.', ',')
                ind_tot = produto['prod'].get('indTot', 'Não informado')
                	
                csosn = 'Não informado'

                regime_tributario = infos_nf['emit'].get('CRT', 'Não informado')

                if regime_tributario == '1' or regime_tributario == '2':
                    icms = produto['imposto'].get('ICMS', {})
                    for chave, valor in icms.items():
                        if isinstance(valor, dict):
                            csosn = valor.get('CSOSN', csosn)
                
                icms = produto['imposto'].get('ICMS', {})
                icms_original = 'Não informado'
                icms_cst = 'Não informado'
                icms_mod_bc = 'Não informado'
                icms_vbc = 'Não informado'
                icms_picms = 'Não informado'
                icms_valor = 'Não informado'

                for chave, valor in icms.items():
                    if isinstance(valor, dict):
                        icms_original = valor.get('orig', icms_original)
                        icms_cst = valor.get('CST', icms_cst)
                        icms_mod_bc = valor.get('modBC', icms_mod_bc)
                        icms_vbc = valor.get('vBC', icms_vbc)
                        if icms_vbc != 'Não informado':
                            icms_vbc = icms_vbc.replace('.', ',')
                        icms_picms = valor.get('pICMS', icms_picms)
                        if icms_picms != 'Não informado':
                            icms_picms = icms_picms.replace('.', ',')
                        icms_valor = valor.get('vICMS', icms_valor)
                        if icms_valor != 'Não informado':
                            icms_valor = icms_valor.replace('.', ',')
                
                ipi = produto['imposto'].get('IPI', {})
                ipi_cst = 'Não informado'
                ipi_vbc = 'Não informado'
                ipi_pipi = 'Não informado'
                ipi_vipi = 'Não informado'

                for chave, valor in ipi.items():
                    if isinstance(valor, dict):
                        ipi_cst = valor.get('CST', ipi_cst)
                        ipi_vbc = valor.get('vBC', ipi_vbc)
                        if ipi_vbc != 'Não informado':
                            ipi_vbc = ipi_vbc.replace('.', ',')
                        ipi_pipi = valor.get('pIPI', ipi_pipi)
                        if ipi_pipi != 'Não informado':
                            ipi_pipi = ipi_pipi.replace('.', ',')
                        ipi_vipi = valor.get('vIPI', ipi_vipi)
                        if ipi_vipi != 'Não informado':
                            ipi_vipi = ipi_vipi.replace('.', ',')

                pis = produto['imposto'].get('PIS', {})
                pis_cst = 'Não informado'
                pis_vbc = 'Não informado'
                pis_ppis = 'Não informado'
                pis_vpis = 'Não informado'

                for chave, valor in pis.items():
                    if isinstance(valor, dict):
                        pis_cst = valor.get('CST', pis_cst)
                        pis_vbc = valor.get('vBC', pis_vbc)
                        if pis_vbc != 'Não informado':
                            pis_vbc = pis_vbc.replace('.', ',')
                        pis_ppis = valor.get('pPIS', pis_ppis)
                        if pis_ppis != 'Não informado':
                            pis_ppis = pis_ppis.replace('.', ',')
                        pis_vpis = valor.get('vPIS', pis_vpis)
                        if pis_vpis != 'Não informado':
                            pis_vpis = pis_vpis.replace('.', ',')

                cofins = produto['imposto'].get('COFINS', {})
                cofins_cst = 'Não informado'
                cofins_vbc = 'Não informado'
                cofins_pcofins = 'Não informado'
                cofins_vcofins = 'Não informado'

                for chave, valor in cofins.items():
                    if isinstance(valor, dict):
                        cofins_cst = valor.get('CST', cofins_cst)
                        cofins_vbc = valor.get('vBC', cofins_vbc)
                        if cofins_vbc != 'Não informado':
                            cofins_vbc = cofins_vbc.replace('.', ',')
                        cofins_pcofins = valor.get('pCOFINS', cofins_pcofins)
                        if cofins_pcofins != 'Não informado':
                            cofins_pcofins = cofins_pcofins.replace('.', ',')
                        cofins_vcofins = valor.get('vCOFINS', cofins_vcofins)
                        if cofins_vcofins != 'Não informado':
                            cofins_vcofins = cofins_vcofins.replace('.', ',')
                        
                valores.append([nome_cliente, cnpj_cliente, fornecedor, cnpj_fornecedor, inscricao_estadual, numero_nota, serie, data_emissao, data_sai_ent, chave_nf, numero_item, cod_produto, ean, nome_produto, ncm, cfop,  quantidade,  valor_unitario,  valor_frete, valor_seguro, valor_desconto, valor_outros, valor_produto, ean_tributado ,unidade_tributada ,quantidade_tributada, valor_unitario_tributado, ind_tot, csosn, icms_original, icms_cst, icms_mod_bc, icms_vbc, icms_picms, icms_valor, ipi_cst, ipi_vbc, ipi_pipi, ipi_vipi ,pis_cst, pis_vbc, pis_ppis, pis_vpis, cofins_cst, cofins_vbc, cofins_pcofins, cofins_vcofins,nome_do_arquivo])

            print("Transação concluída e dados inseridos com sucesso!")

        except Exception as e:
            mensagem_error(f"Erro ao inserir dados: {e}")   

def selecionar_pasta(progresso):
    global sucesso, falha, total_arquivos
    progresso.setValue(0)
    folder_path = QFileDialog.getExistingDirectory(None, "Selecione a pasta com os arquivos XML")
    if not folder_path:
        mensagem_aviso("Nenhuma pasta foi selecionada.")
        return

    lista_arquivos = [os.path.join(folder_path, arquivo) for arquivo in os.listdir(folder_path) if arquivo.endswith('.xml')]

    if not lista_arquivos:
        mensagem_aviso("A pasta selecionada não contém arquivos XML.")
        return

    colunas = ["nome_cliente", "cnpj_cliente", "fornecedor", "cnpj_fornecedor", "inscricao_estadual", "numero_nota", "serie", "data_emissao", "data_sai_ent", "chave_nf", "numero_item", "cod_produto", "ean", "nome_produto", "ncm", "cfop", "quantidade", "valor_unitario", "valor_frete", "valor_seguro", "valor_desconto", "valor_outros", "valor_produto", "ean_tributado", "unidade_tributada", "quantidade_tributada", "valor_unitario_tributado", "ind_tot", "csosn", "icms_original", "icms_cst", "icms_mod_bc", "icms_vbc", "icms_picms", "icms_valor", "ipi_cst", "ipi_vbc", "ipi_pipi", "ipi_vipi","pis_cst", "pis_vbc", "pis_ppis", "pis_vpis", "cofins_cst", "cofins_vbc", "cofins_pcofins", "cofins_vcofins", "nome_do_arquivo"]
    valores = []
    valores_erros = []
    

    try:
        for arquivo in lista_arquivos:
            pegar_infos(arquivo, valores, progresso, lista_arquivos, valores_erros)
    finally:
        print("Processamento concluído")

    tabela = pd.DataFrame(columns=colunas, data=valores)
    tabela_erros = pd.DataFrame(columns=["Arquivo"], data=valores_erros)

    mensagem_sucesso(f"Processamento concluído. Sucesso: {sucesso}, Falha: {falha}, Total de arquivos: {total_arquivos}")
    progresso.setValue(100)

    pergunta = QMessageBox()
    pergunta.setWindowTitle("Salvar arquivo Excel")
    pergunta.setText("Deseja salvar os dados em um arquivo Excel?")
    pergunta.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    pergunta.setDefaultButton(QMessageBox.No)
    pergunta.setStyleSheet("background-color: #001F3F; color: #ffffff; font-size: 16px; font-weight: bold;")
    usar_icone(pergunta)
    
    resposta = pergunta.exec()

    if resposta == QMessageBox.No:
        progresso.setValue(0)
        valores.clear()
        sucesso, falha, total_arquivos = 0, 0, 0
        return
    
    save_path, _ = QFileDialog.getSaveFileName(
        None,
        "Salvar arquivo Excel",
        "",
        "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)"
    )

    if not save_path:
        mensagem_aviso("Nenhum caminho de destino foi selecionado.")
        return

    if not save_path.endswith('.xlsx'):
        save_path += '.xlsx'

    if len(valores_erros) > 0:
        with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
            tabela.to_excel(writer, sheet_name="Dados Processados", index=False)
            tabela_erros.to_excel(writer, sheet_name="Erros", index=False)
    else:
        tabela.to_excel(save_path, index=False, sheet_name="Dados Processados")

    mensagem = QMessageBox()
    mensagem.setWindowTitle("Sucesso")
    mensagem.setText(f"Arquivo Excel gerado com sucesso em:\n{save_path}")
    abrir_botao = mensagem.addButton("Abrir arquivo", QMessageBox.AcceptRole)
    mensagem.addButton("Finalizar", QMessageBox.RejectRole)
    usar_icone(mensagem)

    mensagem.setStyleSheet("""
        * {
            background-color: #001F3F; 
            color: #ffffff; 
            font-size: 16px; 
            font-weight: bold;
        }
        QPushButton {
            padding: 5px 10px; 
            margin: 2px; 
            border-radius: 5px; 
            background-color: #533cbb;
            color: white;
        }
        QPushButton:hover {
            background-color: #362b68;
        }
    """)

    mensagem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    mensagem.exec()

    if mensagem.clickedButton() == abrir_botao:
        os.startfile(save_path)  # Windows
        print(f"Arquivo Excel gerado com sucesso em: {save_path}")
    else:
        print("Processo finalizado.")
    progresso.setValue(0)
    valores.clear()
    sucesso, falha, total_arquivos = 0, 0, 0
    return


def resource_path(relative_path):
    """Obtem o caminho correto para o recurso em qualquer ambiente (Python ou executável)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    app = QtWidgets.QApplication(sys.argv)

    janela = QtWidgets.QMainWindow()
    
    usar_icone(janela)
    
    janela.setWindowTitle("XML")
    janela.setGeometry(100, 100, 800, 600)
    janela.setStyleSheet("background-color: #030d18;")

    widget_central = QtWidgets.QWidget()
    janela.setCentralWidget(widget_central)

    layout = QtWidgets.QVBoxLayout(widget_central)

    botao_frame = QtWidgets.QHBoxLayout()
    layout.addLayout(botao_frame)

    botoes = [
        ("Inserir Pasta com XMLS", lambda: selecionar_pasta(progresso)),
    ]

    for texto, funcao in botoes:
        botao = QtWidgets.QPushButton(texto)
        botao.clicked.connect(funcao)
        botao.setFont(QtGui.QFont("Arial", 14))
        botao.setStyleSheet(""" 
            QPushButton {
                background-color: #001F3F;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #191970;
            }
        """)
        botao.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        botao_frame.addWidget(botao)

    imagem_placeholder = QtWidgets.QLabel()
    imagem_placeholder.setPixmap(QtGui.QPixmap(resource_path("images\\logo.png")).scaled(350, 350, QtCore.Qt.KeepAspectRatio))
    imagem_placeholder.setAlignment(QtCore.Qt.AlignCenter)

    vbox_layout = QtWidgets.QVBoxLayout()
    vbox_layout.addWidget(imagem_placeholder)
    vbox_layout.setAlignment(QtCore.Qt.AlignCenter)

    stack_layout = QtWidgets.QStackedLayout()
    layout.addLayout(stack_layout)

    container_widget = QtWidgets.QWidget()
    container_widget.setLayout(vbox_layout)

    stack_layout.addWidget(container_widget)
    stack_layout.setCurrentWidget(container_widget)

    progresso = QtWidgets.QProgressBar()
    progresso.setRange(0, 100)
    progresso.setValue(0)
    layout.addWidget(progresso)

    janela.showMaximized()
    app.exec()

if __name__ == "__main__":
    main()
