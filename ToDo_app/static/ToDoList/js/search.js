$(document).ready(function() {
    // Отримуємо посилання на форму, поле введення та блок результатів
    var searchForm = $("#search-form");
    var searchInput = $("#search-input");
    var searchResults = $("#search-results");
    var todoList = $("#todo-list"); // Додано блок з завданнями
    var noResults = $("#no-results"); // Додано блок для "Нічого не знайдено"

    // Додамо обробник події для поля введення
    searchInput.on("input", function() {
        // Очищаємо попередні результати
        searchResults.empty();

        // Отримуємо введений текст для пошуку
        var searchText = searchInput.val();

        // Відправляємо Ajax-запит на сервер тільки, якщо введений текст не порожній
        if (searchText.trim() !== "") {
            $.ajax({
                url: "/search_view/", // URL, на який відправити запит
                method: "GET",
                data: { query: searchText }, // Дані для передачі на сервер
                dataType: "html", // Тип отримуваних даних (HTML у нашому випадку)
                success: function(data) {
                    // Вставляємо результати пошуку в блок результатів
                    searchResults.html(data);
                    // Приховуємо список завдань
                    todoList.hide();
                    // Перевіряємо, чи є результати пошуку, і показуємо/приховуємо блок "Нічого не знайдено"
                    if (searchResults.find("li").length === 0) {
                        noResults.show();
                    } else {
                        noResults.hide();
                    }
                }
            });
        } else {
            // Якщо поле пошуку порожнє, показуємо список завдань
            todoList.show();
            noResults.hide();
        }
    });

    // Додамо обробник події для форми пошуку, щоб уникнути її стандартної поведінки
    searchForm.on("submit", function(event) {
        event.preventDefault();
    });
});
