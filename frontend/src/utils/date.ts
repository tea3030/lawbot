export const formatKstDateTime = (value: string | number | Date) => {
  const date = new Date(value);
  return date.toLocaleString("ko-KR", {
    timeZone: "Asia/Seoul",
    hour12: false,
  });
};

export const formatDateTime = (value: string | number | Date) => {
  return formatKstDateTime(value);
};

