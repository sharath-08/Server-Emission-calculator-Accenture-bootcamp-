const RPS = getUrlParam("age");
const time = getUrlParam("seconds");

async function post() {
  const object = {"rps": Number(RPS), "duration": Number(time)};
  const ul = document.getElementById('authors');
  const list = document.createDocumentFragment();
  // const url = 'https://jsonplaceholder.typicode.com/users';
  const url = 'https://cu2yx38yt8.execute-api.ap-southeast-2.amazonaws.com/Prod/simulation';

  await fetch(url, {
    method: 'POST',
    body: JSON.stringify(object)
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let authors = data;
      authors = [authors.body];
      console.log(authors)

      authors.map(function(author) {
        let li = document.createElement('ol');
        let aws_cost = document.createElement('p');
        let aws_emission = document.createElement('p');
        let aws_power = document.createElement('p');
        let cost = document.createElement('p');
        let difference = document.createElement('p');
        let emissions = document.createElement('p');
        let power = document.createElement('p');

        aws_cost.innerHTML = `${"AWS Cost: " + author.aws_cost}`;
        aws_emission.innerHTML = `${"AWS Emission: " + author.aws_emission}`;
        aws_power.innerHTML = `${"AWS Power: " + author.aws_power}`;
        cost.innerHTML = `${"Local Cost: " + author.cost}`;
        difference.innerHTML = `${"Difference: " + author.difference}`;
        emissions.innerHTML = `${"Local Emissions: " + author.emissions}`;
        power.innerHTML = `${"Local Power: " + author.power}`;

        li.appendChild(aws_cost);
        li.appendChild(aws_emission);
        li.appendChild(aws_power);
        li.appendChild(cost);
        li.appendChild(difference);
        li.appendChild(emissions);
        li.appendChild(power);
        list.appendChild(li);
      })
    })
    .then(() => {
        ul.appendChild(list)
    })
    .catch(function(error) {
      console.log(error);
    });
}

post();