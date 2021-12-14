function createOrder(id) {
 
    // Send data to the backend api-view ("order_pizza")
    axios.post('/api/order/', {'id': id})    //This URL is also correct
    .then(res => {
        // Check the Json-Response status, it True, reload the page
        if (res.data.status) {
            var url = "/show_payment/"+id+"/"
            window.location.href = url;
        }
        console.log(res);
    });
}

