export const convertUnixTimestampToDate = (timestamp) => {
  var date = new Date(timestamp * 1000);
  return date.toLocaleDateString("pt-BR");
}