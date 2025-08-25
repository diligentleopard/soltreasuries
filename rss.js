
document.addEventListener("DOMContentLoaded", function () {
  const ticker = document.getElementById("rss-ticker");
  const rssUrl = "https://api.rss2json.com/v1/api.json?rss_url=https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml&q=solana";

  fetch(rssUrl)
    .then(res => res.json())
    .then(data => {
      if (!data.items) return ticker.innerText = "No Solana news found.";
      const headlines = data.items.map(item => `<a href="\${item.link}" target="_blank">\${item.title}</a>`);
      let index = 0;
      ticker.innerHTML = headlines[index];
      setInterval(() => {
        index = (index + 1) % headlines.length;
        ticker.innerHTML = headlines[index];
      }, 5000);
    })
    .catch(err => {
      console.error("RSS Fetch Error:", err);
      ticker.innerText = "Failed to load news.";
    });
});
