const RPS = getUrlParam("age");
const time = getUrlParam("seconds");

async function post() {
  const object = {"rps": Number(RPS), "duration": Number(time)};
  const ul = document.getElementById('authors');
  const list = document.createDocumentFragment();
  // const url = 'https://jsonplaceholder.typicode.com/users';
  const url = 'https://fmpucmr0ll.execute-api.ap-southeast-2.amazonaws.com/Prod/simulation';

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
        let percent = document.createElement('b');

        aws_cost.innerHTML = `${"Cloud Cost of Energy Consumprtion: " + ((author.aws_cost)/100).toLocaleString('en-US') + " dollars"}`;
        aws_emission.innerHTML = `${"Cloud Co2 Emissions: " + author.aws_emission.toLocaleString('en-US') + " grams"}`;
        aws_power.innerHTML = `${"Cloud Power Consumption: " + author.aws_power.toLocaleString('en-US') + " killowats"}`;
        cost.innerHTML = `${"Local Cost of Energy Consumption: " + ((author.cost)/100).toLocaleString('en-US') + " dollars"}`;
        difference.innerHTML = `${"Emissions Difference (Local - Cloud): " + author.difference.toLocaleString('en-US') + " grams"}`;
        emissions.innerHTML = `${"Local Co2 Emissions: " + author.emissions.toLocaleString('en-US') + " grams"}`;
        power.innerHTML = `${"Local Power Consumption: " + author.power.toLocaleString('en-US') + " killowatts"}`;
        percent.innerHTML = `${"There is an approximate " + (author.aws_emission/author.emissions)*100 + "% reduction in Co2 emissions when swtiching to a cloud provider!"}`;

        li.appendChild(power);
        li.appendChild(aws_power);
        li.appendChild(cost);
        li.appendChild(aws_cost);
        li.appendChild(emissions);
        li.appendChild(aws_emission);
        li.appendChild(difference);
        li.appendChild(percent);
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