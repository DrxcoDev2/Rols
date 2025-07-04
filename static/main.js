const htmlString = `
  <div class="card">
    <h2>Hola mundo</h2>
    <p>Este es un componente generado desde una cadena Hola</p>
    
  </div>
`;

// Selecciona el contenedor donde lo quieres insertar
const container = document.getElementById('app');
container.innerHTML = htmlString; // Reemplaza el contenido
