let currentPage = 1;
let totalPages = 1;
let perPage = 10;

function fetchAndRenderUsers(page = 1) {
    const countInput = document.getElementById('countInput').value;
    if (countInput) perPage = parseInt(countInput);

    fetch(`/users/${page}`)
    .then(res => res.json())
    .then(data => {
        const tbody = document.getElementById('peopleTableBody');
        tbody.innerHTML = '';

        data.users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><img src="${user.photo || '#'}" class="img-thumbnail" width="60" /></td>
            <td>${user.gender || ''}</td>
            <td>${user.first_name || ''}</td>
            <td>${user.last_name || ''}</td>
            <td>${user.phone || ''}</td>
            <td>${user.email || ''}</td>
            <td>${user.city || ''}</td>
        `;
        tbody.appendChild(tr);
        });

        currentPage = data.page;
        totalPages = Math.ceil(data.total / data.per_page);
        updatePaginationButtons();
    })
    .catch(err => console.error('Ошибка при загрузке:', err));
}

function updatePaginationButtons() {
    document.getElementById('prevBtn').disabled = currentPage <= 1;
    document.getElementById('nextBtn').disabled = currentPage >= totalPages;
}

function goToPreviousPage() {
    if (currentPage > 1) {
    fetchAndRenderUsers(currentPage - 1);
    }
}

function goToNextPage() {
    if (currentPage < totalPages) {
    fetchAndRenderUsers(currentPage + 1);
    }
}
