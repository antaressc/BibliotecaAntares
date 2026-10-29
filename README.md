# 📚 Biblioteca Antares

Sistema web para gerenciamento da biblioteca corporativa da **Antares**, desenvolvido para facilitar o controle do acervo, usuários, reservas e empréstimos de livros.

## 👨‍💻 Desenvolvedor
**[@luisc5martins](https://github.com/luisc5martins)**

## 🎯 Objetivo

Centralizar e organizar o gerenciamento da biblioteca da empresa, permitindo que colaboradores consultem e reservem livros, enquanto o **RH** administra o acervo, aprova os cadastros e controla as retiradas e devoluções.

## ✨ Funcionalidades

### 👤 Colaboradores

* Cadastro de novos usuários;
* Acompanhamento da aprovação do cadastro;
* Consulta do catálogo de livros;
* Pesquisa por título, autor e categoria;
* Reserva de livros disponíveis;
* Consulta das próprias reservas;
* Consulta dos empréstimos atuais;
* Consulta do histórico de empréstimos.

### 🧑‍💼 RH

* Aprovação ou recusa de cadastros;
* Consulta dos usuários cadastrados;
* Cadastro de novos livros;
* Edição das informações dos livros;
* Controle da disponibilidade dos livros;
* Visualização das reservas;
* Registro da retirada dos livros;
* Registro da devolução dos livros;
* Consulta do histórico de empréstimos.

> **Importante:** livros e registros de empréstimos não são excluídos do sistema. Quando um livro deixa de fazer parte do acervo, sua disponibilidade pode ser alterada, preservando todo o histórico.

## 📖 Controle de empréstimos

Cada empréstimo mantém o histórico das principais etapas:

| Evento    | Informações registradas                |
| --------- | -------------------------------------- |
| Reserva   | Data e hora da reserva                 |
| Retirada  | Data e hora da retirada e responsável  |
| Devolução | Data e hora da devolução e responsável |

Dessa forma, é possível acompanhar todo o ciclo do livro, desde a reserva até sua devolução.

## 🔐 Perfis e permissões

| Ação                        | Colaborador |  RH |
| --------------------------- | :---------: | :-: |
| Criar cadastro              |      ✅      |  ✅  |
| Aprovar usuário             |      ❌      |  ✅  |
| Recusar usuário             |      ❌      |  ✅  |
| Consultar livros            |      ✅      |  ✅  |
| Reservar livro              |      ✅      |  ✅  |
| Cadastrar livro             |      ❌      |  ✅  |
| Editar livro                |      ❌      |  ✅  |
| Excluir livro               |      ❌      |  ❌  |
| Registrar retirada          |      ❌      |  ✅  |
| Registrar devolução         |      ❌      |  ✅  |
| Consultar próprio histórico |      ✅      |  ✅  |
| Consultar histórico geral   |      ❌      |  ✅  |

## 🛠️ Tecnologias

* **Python**
* **PDM**
* **Banco de dados relacional**
* **HTML5**

## 🚦 Status do projeto

🟢 **Em produção**

O sistema Biblioteca Antares está implantado e em utilização na empresa. O projeto encontra-se em manutenção e evolução contínuas, com correções, melhorias e implementação de novas funcionalidades conforme as necessidades identificadas.

## 📌 Regras importantes

* O cadastro de novos colaboradores depende de aprovação do RH.
* Somente usuários aprovados podem utilizar o sistema.
* O RH é responsável pelo gerenciamento do acervo.
* O RH pode **inserir e editar livros**, mas não pode excluí-los.
* Retiradas e devoluções são registradas pelo RH.
* O histórico de reservas e empréstimos deve ser preservado.
* A data e hora das reservas, retiradas e devoluções são registradas no sistema.

## 👨‍🏫 Agradecimentos

Agradeço aos professores **[@marrcandre](https://github.com/marrcandre)** e **[@eduardo-da-silva](https://github.com/eduardo-da-silva)**, que fizeram parte da minha formação e contribuíram para minha trajetória na área de tecnologia.

O projeto utiliza como base o **template disponibilizado por [@marrcandre](https://github.com/marrcandre)** e teve como material de apoio os **vídeos e tutoriais disponibilizados por [@eduardo-da-silva](https://github.com/eduardo-da-silva)**.

---

**Biblioteca Antares**
Sistema interno para gerenciamento do acervo e empréstimos da biblioteca corporativa.
