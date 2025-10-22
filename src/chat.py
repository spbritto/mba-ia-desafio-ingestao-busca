import os 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from search import PROMPT_TEMPLATE

# Carrega as variáveis de ambiente
load_dotenv()
for k in("OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

# Configuração dos embeddings
embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

# Configuração do PGVector store
store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
)

# Configuração do modelo LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

# Configuração do prompt template
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Criação da chain: prompt -> llm -> parser
chain = prompt | llm | StrOutputParser()

def main():
    """CLI para interação com o usuário via chat"""
    
    print("=" * 60)
    print("CHAT COM DOCUMENTOS PDF")
    print("=" * 60)
    print("Faça suas perguntas sobre o documento.")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        # Solicita a pergunta do usuário
        pergunta = input("\nPERGUNTA: ").strip()
        
        # Verifica se o usuário quer sair
        if pergunta.lower() in ['sair', 'exit', '']:
            print("\nEncerrando. Até logo!")
            break
        
        try:
            # Passo 1: Busca os documentos mais relevantes (k=10)
            results = store.similarity_search_with_score(pergunta, k=10)
            
            # Passo 2: Monta o contexto com os documentos encontrados
            contexto_parts = []
            for i, (doc, score) in enumerate(results, start=1):
                contexto_parts.append(f"[Documento {i}]:\n{doc.page_content}")
            
            contexto = "\n\n".join(contexto_parts)
            
            # Passo 3: Chama a chain com o contexto e a pergunta
            resposta = chain.invoke({
                "contexto": contexto,
                "pergunta": pergunta
            })
            
            # Passo 4: Exibe a resposta
            print(f"RESPOSTA: {resposta}")
            
        except Exception as e:
            print(f"Erro ao processar: {e}")

if __name__ == "__main__":
    main()