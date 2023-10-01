import sqlalchemy
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'clientes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nome = sqlalchemy.Column(sqlalchemy.String)
    cpf = sqlalchemy.Column(sqlalchemy.String)
    endereco = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    conta = sqlalchemy.orm.relationship('Conta', back_populates='cliente', uselist=False, cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f'Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco}, email={self.email})'
    
    def __str__(self):
        return f'Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco}, email={self.email})'
    
class Conta(Base):
    __tablename__ = 'contas'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    tipo = sqlalchemy.Column(sqlalchemy.String)
    agencia = sqlalchemy.Column(sqlalchemy.String)
    numero = sqlalchemy.Column(sqlalchemy.String)
    saldo = sqlalchemy.Column(sqlalchemy.Float)
    cliente_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clientes.id'))
    cliente = sqlalchemy.orm.relationship('Cliente', back_populates='conta', uselist=False)

    def __repr__(self):
        return f'Conta(id={self.id}, numero={self.numero}, saldo={self.saldo}, cliente_id={self.cliente_id})'
    
    def __str__(self):
        return f'Conta(id={self.id}, numero={self.numero}, saldo={self.saldo}, cliente_id={self.cliente_id})'
    
# Cria o banco de dados
engine = sqlalchemy.create_engine('sqlite://')

# Cria as tabelas
Base.metadata.create_all(engine)

# Investiga o banco de dados
Inspector = sqlalchemy.inspect(engine)

with sqlalchemy.orm.Session(engine) as session:
    # Cria um cliente
    cleiton = Cliente(nome='cleiton', 
                      cpf='111.111.111-11', 
                      endereco='Rua A, 123',
                      email='dev@cleitonmachado.com', 
                      conta=Conta(tipo='corrente', 
                                  agencia='0001', 
                                  numero='1234-5', 
                                  saldo=1000.00))
    
    vanessa = Cliente(nome='vanessa', 
                      cpf='000.000.000-0', 
                      endereco='Rua A, 123',
                      email='vanessa@cleitonmachado.com', 
                      conta=Conta(tipo='corrente', 
                                  agencia='0001', 
                                  numero='2234-5', 
                                  saldo=1000.00))
    

    # Adiciona o cliente ao banco de dados
    session.add_all([cleiton, vanessa])

    # Confirma a transação
    session.commit()

stmt = sqlalchemy.select(Cliente)
conection = engine.connect()
result = conection.execute(stmt).fetchall()
for result in result:
    print(result)

