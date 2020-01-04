function fetchData(id) {
    return new Promise((resolve, reject) => {
      const req = new XMLHttpRequest();
      req.onreadystatechange = function(event) {
          if (this.readyState === XMLHttpRequest.DONE) {
              if (this.status === 200) {
                resolve(JSON.parse(this.responseText));
              } else {
                  reject("Status de la réponse: %d (%s)", this.status, this.statusText);
              }
          }
      };
  
      req.open('GET', '/api/meter/' + id + '/journal', true);
      req.send(null);
    });
}