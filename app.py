from flask import Flask, render_template, jsonify, request, redirect , url_for , flash , session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:laura@localhost:5432/Trabalho_PBD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Compra(db.Model):
    __tablename__ = 'compra'
    id_compra = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    valor_total = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('compras', lazy=True))

    def __repr__(self):
        return f'<Compra {self.id_compra} - {self.status}>'

class Carrinho(db.Model):
    id_carrinho = db.Column(db.Integer , primary_key = True)
    id_cliente = db.Column(db.Integer , nullable = False)

class Estoque(db.Model):
    __tablename__ = 'estoque'
    id_estoque = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    
    produto = db.relationship('Produto', backref=db.backref('estoque_info', uselist=False))

    def __repr__(self):
        return f'<Estoque Produto {self.id_estoque} - Qtd: {self.quantidade}>'

class Item_Carrinho(db.Model):
    __tablename__ = 'item_carrinho'
    __table_args__ = (
        db.PrimaryKeyConstraint('id_carrinho', 'id_produto'),  # Define a PK composta
    )

    # Remove 'id_item_carrinho' (não existe no banco)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    id_carrinho = db.Column(db.Integer, db.ForeignKey('carrinho.id_carrinho'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id_produto'), nullable=False)

    # Mantenha os relacionamentos (opcional, se já existiam)
    carrinho = db.relationship('Carrinho', backref=db.backref('itens', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('itens', lazy=True))

class Produto(db.Model):
    __tablename__ = 'produto'  
    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True, default = 1)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50))

    def __repr__(self):
        return f'<Produto {self.nome}>'
    
class Cliente(db.Model):
    id_cliente = db.Column(db.Integer , primary_key = True)
    nome = db.Column(db.String(100) , nullable = False)
    email = db.Column(db.String(255) , unique = True , nullable = False)
    senha_hash = db.Column(db.String(255) , nullable = False)
    estado = db.Column(db.String(50) , nullable = False)
    cidade = db.Column(db.String(100) , nullable = False)
    bairro = db.Column(db.String(100) , nullable = False)
    numero = db.Column(db.String(10) , nullable = False)
    rua = db.Column(db.String(255) , nullable = False)

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    if 'id_cliente' not in session:
        return jsonify({'error': 'Você precisa estar logado para finalizar a compra.'}), 401

    cliente_id = session['id_cliente']
    carrinho = Carrinho.query.filter_by(id_cliente=cliente_id).first()
    
    if not carrinho or not carrinho.itens:
        return jsonify({'error': 'Seu carrinho está vazio.'}), 400

    try:
        # Verificar estoque antes de processar
        for item in carrinho.itens:
            estoque = Estoque.query.get(item.id_produto)
            if not estoque or estoque.quantidade < item.quantidade:
                produto = Produto.query.get(item.id_produto)
                disponivel = estoque.quantidade if estoque else 0
                return jsonify({
                    'error': f'Estoque insuficiente para {produto.nome}. Disponível: {disponivel}'
                }), 400

        # Calcular valor total
        valor_total = sum(item.produto.preco * item.quantidade for item in carrinho.itens)
        
        # Criar a compra
        nova_compra = Compra(
            status='concluída',
            valor_total=valor_total,
            id_cliente=cliente_id
        )
        db.session.add(nova_compra)

        # Atualizar estoque e processar itens
        for item in carrinho.itens:
            estoque = Estoque.query.get(item.id_produto)
            estoque.quantidade -= item.quantidade  # Reduz o estoque

        # Limpar carrinho
        Item_Carrinho.query.filter_by(id_carrinho=carrinho.id_carrinho).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Compra finalizada com sucesso! Estoque atualizado.',
            'compra_id': nova_compra.id_compra,
            'valor_total': valor_total
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao finalizar compra: {str(e)}'}), 500


@app.route('/add_usuario' , methods=['POST'])
def add_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha_hash = request.form['senha']  # Em produção, use hash para armazenar senha!
    estado = request.form['estado']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    numero = request.form['numero']
    rua = request.form['rua']

    novo_usuario = Cliente(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        estado=estado,
        cidade=cidade,
        bairro=bairro,
        numero=numero,
        rua=rua
    )

    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/remover_item/<int:id_produto>', methods=['POST'])
def remover_item(id_produto):
    if 'id_cliente' not in session:
        return jsonify({'error': 'Não autorizado'}), 401

    cliente_id = session['id_cliente']
    carrinho = Carrinho.query.filter_by(id_cliente=cliente_id).first()
    
    if not carrinho:
        return jsonify({'error': 'Carrinho não encontrado'}), 404

    item = Item_Carrinho.query.filter_by(
        id_carrinho=carrinho.id_carrinho,
        id_produto=id_produto
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item removido do carrinho'})
    
    return jsonify({'error': 'Item não encontrado no carrinho'}), 404

@app.route('/userlogin' , methods = ['GET' , 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        cliente = Cliente.query.filter_by(email=email).first()
        if cliente:
            if cliente.senha_hash==senha:
                session['id_cliente'] = cliente.id_cliente
                flash('Login bem-sucedido!' , 'success')
                return redirect(url_for('home'))
            else:
                flash('Senha Incorreta!' , 'danger')
        else:
            flash('Usuário não encontrado!' , 'danger')
    return redirect(url_for('login'))


# Mapeamento manual de imagens
IMAGENS_PRODUTOS = {
    1: "https://images.tcdn.com.br/img/img_prod/802666/camiseta_masculina_basica_manga_curta_algodao_anticorpus_41_1_c47a00aeb08e0c011618250b79e40cc1.jpg",
    2: "https://images.tcdn.com.br/img/img_prod/980126/vestido_longo_primavera_verao_flores_estampado_preto_1463_1_32240b3fd43e0a2d6620161f32de38c1.jpeg",
    3: "https://www.revanche.com.br/media/catalog/product/cache/8e5872966dd88cc0e998d2d2c4eec43a/c/a/cal_a-jeans-skinny-fit-belt-atacado-feminina-revanche-taba_201017-_6_-1.jpg",
    4: "https://img.irroba.com.br/filters:fill(fff):quality(80)/elitiaue/catalog/010/elitecourodscf0677.jpg",
    5: "https://images.tcdn.com.br/img/img_prod/1065474/blusa_feminina_tricot_gola_alta_4676_1_6e81d99bac8716a5cd792cf79914e041.jpg",
    6: "https://images.tcdn.com.br/img/img_prod/787274/tenis_esportivo_feminino_acqua_pessego_olympikus_12602_1_423190dc2e18ca0cdfb28935618fa51c.jpg",
    7: "https://acdn-us.mitiendanube.com/stores/003/063/828/products/saia-tule-floral-2-1b2554317b925fa0a216991171364285-1024-1024.jpg",
    8: "https://ph-cdn3.ecosweb.com.br/imagens01/foto/mkp202/moda-feminina/shorts/shorts-jeans-mom-feminino-cintura-alta-com-prega-azul_2321519_600_1.jpg",
    9: "https://hiatto.cdn.magazord.com.br/img/2023/07/produto/10180/01m0012-006-camiseta-masculina-justin-black-marinho-3.png?ims=630x945",
    10: "https://images.tcdn.com.br/img/img_prod/1167684/bermuda_esporte_casual_polialgodao_e_elastano_acetinado_996_1_7bca9346423e7ba975707beb200448bc.jpg"
}

# Rota que retorna os produtos com a URL da imagem
@app.route('/api/produtos')
def api_produtos():
    produtos = Produto.query.all()
    produtos_list = []
    for produto in produtos:
        estoque = Estoque.query.get(produto.id_produto)
        produtos_list.append({
            'id_produto': produto.id_produto,
            'nome': produto.nome,
            'preco': produto.preco,
            'estoque': estoque.quantidade if estoque else 0,
            'categoria': produto.categoria,
            'imagem': IMAGENS_PRODUTOS.get(produto.id_produto, "https://via.placeholder.com/150")
        })
    return jsonify(produtos_list)

def register_new_user():
    nome = request.form('nome')
    email = request.form('email')
    senha = request.form('senha')
    estado = request.form('estado')
    cidade = request.form('cidade')
    bairro = request.form('bairro')
    numero = request.form('numero')
    rua = request.form('rua')

    if not (nome and email and senha and estado and cidade and bairro and numero and rua):
        return jsonify({'error':'Todos os campos são obrigatórios!'}),400

@app.route('/adicionar_carrinho/<int:id_produto>', methods=['POST'])
def adicionar_ao_carrinho(id_produto):
    if 'id_cliente' not in session:
        return jsonify({'error': 'Você precisa estar logado para adicionar itens ao carrinho.'}), 401

    # Verifica se o produto existe
    produto = Produto.query.get(id_produto)
    if not produto:
        return jsonify({'error': f'Produto com ID {id_produto} não encontrado.'}), 404

    # Obtém os dados da requisição
    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Dados inválidos.'}), 400

    # Pega o valor enviado (novamente, esse valor representa a quantidade desejada)
    nova_quantidade = dados.get('quantidade', 1)

    # Obtém ou cria o carrinho do cliente
    cliente_id = session['id_cliente']
    carrinho = Carrinho.query.filter_by(id_cliente=cliente_id).first()
    if not carrinho:
        carrinho = Carrinho(id_cliente=cliente_id)
        db.session.add(carrinho)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao criar carrinho: {str(e)}'}), 500

    # Verifica se o item já existe no carrinho
    item = Item_Carrinho.query.filter_by(
        id_carrinho=carrinho.id_carrinho,
        id_produto=id_produto
    ).first()

    if item:
        # Atualiza a quantidade para o novo valor (não soma)
        item.quantidade = nova_quantidade
    else:
        item = Item_Carrinho(
            id_carrinho=carrinho.id_carrinho,
            id_produto=id_produto,
            quantidade=nova_quantidade
        )
        db.session.add(item)

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Produto {produto.nome} adicionado/atualizado no carrinho!',
            'produto': {
                'id': produto.id_produto,
                'nome': produto.nome,
                'preco': produto.preco
            },
            'quantidade': nova_quantidade
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao adicionar/atualizar item: {str(e)}'}), 500

# Rota para a página inicial
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/ver_carrinho')
def ver_carrinho():
    if 'id_cliente' not in session:
        return jsonify({'error': 'Usuário não logado'}), 401

    cliente_id = session['id_cliente']
    carrinho = Carrinho.query.filter_by(id_cliente=cliente_id).first()

    if not carrinho:
        return jsonify({'itens': []})

    # Carrega explicitamente os itens e produtos relacionados
    itens = db.session.query(Item_Carrinho, Produto)\
        .join(Produto, Item_Carrinho.id_produto == Produto.id_produto)\
        .filter(Item_Carrinho.id_carrinho == carrinho.id_carrinho)\
        .all()

    itens_formatados = []
    for item, produto in itens:
        itens_formatados.append({
            'id_produto': produto.id_produto,
            'nome': produto.nome,
            'preco': float(produto.preco),
            'quantidade': item.quantidade,
            'total': float(produto.preco * item.quantidade),
            'imagem': IMAGENS_PRODUTOS.get(produto.id_produto, "https://via.placeholder.com/150")
        })

    return jsonify({
        'itens': itens_formatados,
        'debug': {
            'cliente_id': cliente_id,
            'carrinho_id': carrinho.id_carrinho if carrinho else None,
            'total_itens': len(itens_formatados)
        }
    })
    
if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas se não existirem
        db.create_all()
        
        # Configura a sequência para começar em 1 (PostgreSQL)
        if db.engine.name == 'postgresql':
            try:
                # Primeiro tenta atualizar a versão de collation
                db.session.execute(text("ALTER DATABASE \"Trabalho_PBD\" REFRESH COLLATION VERSION"))
                db.session.commit()
                print("Versão de collation atualizada com sucesso.")
            except Exception as collation_error:
                print(f"Aviso: Não foi possível atualizar a versão de collation: {collation_error}")
                db.session.rollback()
            
            try:
                # Configura a sequência do ID do produto
                db.session.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'produto_id_produto_seq') THEN
                            CREATE SEQUENCE produto_id_produto_seq START 1;
                        ELSE
                            ALTER SEQUENCE produto_id_produto_seq RESTART WITH 1;
                        END IF;
                    END $$;
                """))
                db.session.commit()
                print("Sequência do produto configurada para começar em 1.")
            except Exception as seq_error:
                print(f"Erro ao configurar sequência: {seq_error}")
                db.session.rollback()
    
    app.run(debug=True)
