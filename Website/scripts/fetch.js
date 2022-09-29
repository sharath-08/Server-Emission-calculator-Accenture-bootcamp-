console.log("cookie")

var obj;

fetch('https://reqres.in/api/users/').then(res => { return res.json() }).then(data => obj = data).then(() => console.log(obj))
    .then(data => console.log(data)).catch(error => console.log("ERROR"));