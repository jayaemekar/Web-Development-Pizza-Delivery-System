function createOrder(id) {
     alert(`Order Placed Successfully !`);

    // Send data to the backend api-view ("order_pizza")
    axios.post('/api/order/', {'id': id})    //This URL is also correct
   // axios.post( 'http://127.0.0.1:8080/api/order/', {'id': id} )
    .then(res => {
        // Check the Json-Response status, it True, reload the page
        if (res.data.status) {
            // window.location.reload();

            // Redirecting the user to the order-list page
           // var url = "http://127.0.0.1:8080/order_list/"
            var url = "/order_list/"
            window.location.href = url;
        }
        console.log(res);
    });
}

