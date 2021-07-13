const $guessForm = $('#guess-form');
$guessForm.on('submit', async function(evt){
    evt.preventDefault();
    let response = await axios.get('/guess', {'params': {'guess': $('#guess').val()}});
    return response;
})
