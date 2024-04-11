export const convertUnixTimestampToDate = (timestamp) => {
  var date = new Date(timestamp * 1000);
  return date.toLocaleDateString("pt-BR");
}

export const toBRL = (value) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
}

export const stringToDateTime = (value) => {
  return new Date(value).toLocaleDateString("pt-BR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}