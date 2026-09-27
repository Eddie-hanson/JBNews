(function () {
  const input = document.getElementById("search-input");
  const dropdown = document.getElementById("search-results");
  const inner = document.getElementById("search-results-inner");
  let timer = null;

  if (!input) return; // guard — exits if element not found

  function show(html) {
    inner.innerHTML = html;
    dropdown.classList.add("active");
  }

  function hide() {
    dropdown.classList.remove("active");
    inner.innerHTML = "";
  }

  input.addEventListener("input", function () {
    clearTimeout(timer);
    const q = this.value.trim();

    if (q.length < 2) {
      hide();
      return;
    }

    show('<p class="search-loading">Searching...</p>');

    timer = setTimeout(function () {
      fetch("/search/?q=" + encodeURIComponent(q))
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (!data.results.length) {
            show('<p class="search-no-results">No results found.</p>');
            return;
          }

          var html = data.results
            .map(function (a) {
              return (
                '<a class="search-result-item" href="' +
                a.url +
                '">' +
                (a.picture
                  ? '<img class="search-result-img" src="' +
                    a.picture +
                    '" alt="">'
                  : "") +
                '<span class="search-result-title">' +
                a.title +
                "</span>" +
                "</a>"
              );
            })
            .join("");

          show(html);
        })
        .catch(function () {
          show('<p class="search-no-results">Something went wrong.</p>');
        });
    }, 300);
  });

  document.addEventListener("click", function (e) {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      hide();
    }
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });
})();
