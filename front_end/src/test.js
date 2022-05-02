
async function getGithubData() {

  const axios = require('axios');

  axios.get('https://rumzon-db.herokuapp.com/rumzon/items/all')
    .then(res => {
        console.log(res.data);
    })
    .catch(err => {
        console.log(err);
    });
}

getGithubData();