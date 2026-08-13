// ===== LÓGICA DOS BOTÕES DE AJUDA (?) =====
// Controla a abertura e fechamento dos tooltips contextuais
// nos campos do formulário de ciclo de estudo.
 
(function () {
    let tooltipAtivo = null;
 
    function fecharTooltip() {
        if (tooltipAtivo) {
            tooltipAtivo.remove();
            tooltipAtivo = null;
        }
        document.querySelectorAll('.btn-ajuda.ativo').forEach(function (btn) {
            btn.classList.remove('ativo');
        });
    }
 
    function abrirTooltip(btn) {
        const texto = btn.getAttribute('data-tooltip');
        if (!texto) return;
 
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-ajuda';
        tooltip.textContent = texto;
        tooltip.setAttribute('role', 'tooltip');
 
        // Insere o tooltip dentro do .label-com-ajuda (pai do botão)
        const container = btn.parentElement;
        container.appendChild(tooltip);
 
        tooltipAtivo = tooltip;
        btn.classList.add('ativo');
    }
 
    document.querySelectorAll('.btn-ajuda').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation();
 
            // Se o tooltip deste botão já está aberto, fecha
            if (btn.classList.contains('ativo')) {
                fecharTooltip();
                return;
            }
 
            // Fecha qualquer outro tooltip aberto e abre o novo
            fecharTooltip();
            abrirTooltip(btn);
        });
    });
 
    // Clique fora fecha o tooltip
    document.addEventListener('click', function () {
        fecharTooltip();
    });
 
    // ESC também fecha
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') fecharTooltip();
    });
})();
 