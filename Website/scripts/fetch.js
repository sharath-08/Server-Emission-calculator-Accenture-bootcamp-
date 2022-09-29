const ul = document.getElementById('authors');
      const list = document.createDocumentFragment();
      const url = 'https://jsonplaceholder.typicode.com/users';
    
      fetch(url)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          let authors = data;
          console.log(authors)
    
          authors.map(function(author) {
            let li = document.createElement('li');
            let name = document.createElement('h2');
            let email = document.createElement('span');
    
            name.innerHTML = `${author.name}`;
            email.innerHTML = `${author.email}`;
    
            li.appendChild(name);
            li.appendChild(email);
            list.appendChild(li);
          })
        })
        .then(() => {
            ul.appendChild(list)
        })
        .catch(function(error) {
          console.log(error);
        });