$(document).ready(function () {
    // Enviar a mensagem ao pressionar Enter
    $('#pergunta').on('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            $('#chat-form').submit();
        }
    });

    $('#chat-form').on('submit', function (e) {
        e.preventDefault();
        var pergunta = $('#pergunta').val();
        if (pergunta.trim() === '') {
            return;
        }
        var timestamp = new Date();
        var hours = timestamp.getHours().toString().padStart(2, '0');
        var minutes = timestamp.getMinutes().toString().padStart(2, '0');
        var timeString = hours + ':' + minutes;

        var userMessage = '<div class="message user-message"><p class="message-title">Usuário</p><p>' + $('<div/>').text(pergunta).html() + '</p><span class="timestamp">' + timeString + '</span></div>';
        $('#chat-container').append(userMessage);
        $('#pergunta').val('');
        var botMessage = '<div class="message system-message"><p class="message-title">Sistema</p><p>Respondendo<span class="dot-animated"></span></p><span class="timestamp">' + timeString + '</span></div>';
        $('#chat-container').append(botMessage);
        $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);

        $.ajax({
            url: '/get_response',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'pergunta': pergunta }),
            success: function (data) {
                if (data.resposta) {
                    $('#chat-container .message.system-message:last p:nth-of-type(2)').html(data.resposta);
                    // Atualizar o timestamp
                    var timestamp = new Date();
                    var hours = timestamp.getHours().toString().padStart(2, '0');
                    var minutes = timestamp.getMinutes().toString().padStart(2, '0');
                    var timeString = hours + ':' + minutes;
                    $('#chat-container .message.system-message:last .timestamp').text(timeString);
                    $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
                } else if (data.erro) {
                    $('#chat-container .message.system-message:last p:nth-of-type(2)').html(data.erro);
                }
            },
            error: function () {
                $('#chat-container .message.system-message:last p:nth-of-type(2)').html('Erro ao obter resposta.');
            }
        });
    });
});