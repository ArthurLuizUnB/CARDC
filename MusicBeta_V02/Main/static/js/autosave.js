// MusicBeta_V02/Main/static/js/autosave.js
// Gerencia o salvamento automático (Auto-save) com balão flutuante e buffer de inatividade.

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-ciclo');
    const toast = document.getElementById('autosave-toast');
    const inputCicloId = document.getElementById('ciclo_id_autosave');
    const tituloPagina = document.getElementById('titulo-pagina-ciclo');
    const btnVoltar = document.getElementById('btn-voltar-biblioteca');
    const chkTerminado = document.getElementById('terminado');
    const labelFinalizar = document.getElementById('label-finalizar-card');
    const textoFinalizar = document.getElementById('texto-finalizar-status');

    if (!form || !toast) return;

    const TEMPO_IDLE_MS = 6000; // 6 segundos de inatividade antes de salvar
    let timerDebounce = null;
    let timerOcultarToast = null;
    let alteracoesPendentes = false;

    const camposIds = [
        'obra', 'compositor', 'data_inicio', 'data_finalizacao',
        'consideracoes_preliminares', 'acao_artistica', 'descricao_tarefa',
        'resultado_tecnico', 'resultado_musical', 'observacoes',
        'pensamentos_associados', 'emocoes_associadas', 'diario_reflexivo'
    ];

    function mostrarToast(texto, estado, autoOcultar = false) {
        clearTimeout(timerOcultarToast);
        toast.textContent = texto;
        toast.className = `autosave-toast visivel ${estado || ''}`;

        if (autoOcultar) {
            timerOcultarToast = setTimeout(() => {
                toast.classList.remove('visivel');
            }, 3200);
        }
    }

    function atualizarVisualFinalizar() {
        if (!chkTerminado || !labelFinalizar || !textoFinalizar) return;
        if (chkTerminado.checked) {
            labelFinalizar.classList.add('ativo');
            textoFinalizar.textContent = 'Ciclo marcado como finalizado';
        } else {
            labelFinalizar.classList.remove('ativo');
            textoFinalizar.textContent = 'Marcar ciclo como finalizado';
        }
    }

    function montarPayload() {
        const payload = { ciclo_id: inputCicloId.value };
        camposIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) payload[id] = el.value;
        });
        payload.terminado = chkTerminado ? chkTerminado.checked : false;
        return payload;
    }

    async function executarAutosave() {
        clearTimeout(timerDebounce);
        alteracoesPendentes = false;
        mostrarToast('Salvando ciclo...', 'salvando', false);

        const payload = montarPayload();

        try {
            const resp = await fetch('/ciclo/autosave', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const dados = await resp.json();

            if (resp.ok && dados.sucesso) {
                if (dados.novo && dados.ciclo_id) {
                    inputCicloId.value = dados.ciclo_id;
                    form.action = '/ciclo/editar/' + dados.ciclo_id;
                    window.history.replaceState(null, '', '/ciclo/editar/' + dados.ciclo_id);
                }
                if (payload.obra && payload.obra.trim() && tituloPagina) {
                    tituloPagina.textContent = 'Editando: ' + payload.obra.trim();
                }
                mostrarToast('✓ Ciclo salvo', 'salvo', true);
                return true;
            } else {
                mostrarToast('⚠️ Erro ao salvar ciclo', 'erro', false);
                return false;
            }
        } catch (e) {
            mostrarToast('⚠️ Sem conexão para salvar', 'erro', false);
            return false;
        }
    }

    function agendarAutosave() {
        alteracoesPendentes = true;
        clearTimeout(timerDebounce);
        timerDebounce = setTimeout(executarAutosave, TEMPO_IDLE_MS);
    }

    camposIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', agendarAutosave);
    });

    if (chkTerminado) {
        atualizarVisualFinalizar();
        chkTerminado.addEventListener('change', () => {
            atualizarVisualFinalizar();
            executarAutosave(); // Quando clica em finalizar, já salva na hora!
        });
    }

    // Se o usuário clicar em "Voltar para a Biblioteca" antes dos 6 segundos, salva imediatamente antes de sair
    if (btnVoltar) {
        btnVoltar.addEventListener('click', async (event) => {
            const videoInput = document.getElementById('video_upload');
            const temVideoSelecionado = videoInput && videoInput.files && videoInput.files.length > 0;

            if (temVideoSelecionado) {
                event.preventDefault();
                form.submit();
                return;
            }

            if (alteracoesPendentes) {
                event.preventDefault();
                const destino = btnVoltar.href;
                await executarAutosave();
                window.location.href = destino;
            }
        });
    }
});
