// MusicBeta_V02/Main/static/js/biblioteca.js
// Gerencia o menu de 3 barras, confirmações e o modal de exportação na Biblioteca (home.html).

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-exportar');
    const subtituloModal = document.getElementById('export-modal-subtitle');
    const linkPdf = document.getElementById('link-export-pdf');
    const linkDocx = document.getElementById('link-export-docx');
    const linkTxt = document.getElementById('link-export-txt');

    function fecharTodosMenus(excetoId = null) {
        document.querySelectorAll('.cycle-dropdown.aberto').forEach(menu => {
            if (menu.id !== excetoId) {
                menu.classList.remove('aberto');
            }
        });
    }

    function fecharModalExportacao() {
        if (modal && modal.open) {
            modal.close();
        }
    }

    // 1. Botões de 3 barras para abrir/fechar o menu de opções do ciclo
    document.querySelectorAll('[data-menu-target]').forEach(botao => {
        botao.addEventListener('click', (event) => {
            event.stopPropagation();
            const menuId = botao.dataset.menuTarget;
            fecharTodosMenus(menuId);
            const menuAlvo = document.getElementById(menuId);
            if (menuAlvo) {
                menuAlvo.classList.toggle('aberto');
            }
        });
    });

    // 2. Opção "Exportar documento..." dentro do menu do ciclo
    document.querySelectorAll('.item-export[data-ciclo-id]').forEach(botao => {
        botao.addEventListener('click', () => {
            const cicloId = botao.dataset.cicloId;
            const tituloCiclo = botao.dataset.cicloTitulo || '';

            fecharTodosMenus();
            if (subtituloModal) subtituloModal.textContent = tituloCiclo;
            if (linkPdf) linkPdf.href = `/ciclo/exportar/${cicloId}/pdf`;
            if (linkDocx) linkDocx.href = `/ciclo/exportar/${cicloId}/docx`;
            if (linkTxt) linkTxt.href = `/ciclo/exportar/${cicloId}/txt`;

            if (modal) modal.showModal();
        });
    });

    // 3. Confirmação de exclusão sem usar onclick inline no HTML
    document.querySelectorAll('[data-confirm]').forEach(link => {
        link.addEventListener('click', (event) => {
            if (!window.confirm(link.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });

    // 4. Botões e cartões que fecham o modal de exportação
    document.querySelectorAll('[data-close-modal]').forEach(el => {
        el.addEventListener('click', fecharModalExportacao);
    });

    // 5. Fechar menus ao clicar fora e fechar modal ao clicar no fundo (backdrop)
    document.addEventListener('click', () => fecharTodosMenus());

    if (modal) {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                fecharModalExportacao();
            }
        });
    }
});
