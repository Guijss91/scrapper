Endpoints

GET - http://127.0.0.1:5000

POST - http://127.0.0.1:5000/scrap  

  Parametros:  
  
  {
    "url": "https://www.jusbrasil.com.br/jurisprudencia/busca?q=alimentos", 
    "fields": ["body", "links", "header"],                                // Pode usar apenas um dos parametros
    "follow_links": 3,                                                    // quantidade de links retornados que serão raspados
    "ignore_external": true,                                              // ignorar links externos - default true
    "depth": 1                                                            // profundidade da camada de links que serão raspados
}

  
