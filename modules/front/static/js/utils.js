export const convertUnixTimestampToDate = (timestamp) => {
  var date = new Date(timestamp * 1000);
  return date.toLocaleDateString("pt-BR");
}

export const toBRL = (value) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
}