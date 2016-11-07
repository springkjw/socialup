var nickname = null;
var userId = null;
var currentUser;
var currentChannel = null;
var messageList = [];
var lastUpdated = new Date(0);

/***********************************************
 *                MESSAGING
 **********************************************/

function addMessage(message) {
    if (diffInDay(lastUpdated.getTime(), message.createdAt) != 0) {
        var createdAt = new Date(message.createdAt);
        $('#chat-messages').append('<label>{}</label>'.format(getDateString(createdAt)));

        lastUpdated = createdAt;
    }

    var messageClass = 'message';
    if (message.sender.userId == currentUser.userId) {
        messageClass += ' right';
    }

    var messageBody;
    if (message.isFileMessage()) {
        $('.chat-input-file').removeClass('file-upload');
        $('#chat_file_input').val('');

        messageBody = '<a href="{}" class="filename" target="_blank">{}</a>'.format(message.url, message.name);
    }
    else {
        messageBody = message.message;
    }

    var messageString =
        ('<div class="{}">' +
            '<img src="{}"><div class="bubble">{}<div class="corner"></div><span>{}</span></div>' +
        '</div>').format(
            messageClass,
            message.sender.profileUrl,
            messageBody,
            getTimeString(message.createdAt)
        );
    $('#chat-messages').append(messageString);

    scrollPositionBottom();
}

$('#chat-input-text').keydown(function(event) {
    if (event.keyCode == 13 && !event.shiftKey) {
        event.preventDefault();
        if (!$.trim(this.value).isEmpty()) {
            event.preventDefault();
            this.value = $.trim(this.value);

            currentChannel.sendUserMessage($.trim(this.value), '', SendMessageHandler);
            scrollPositionBottom();
        }
        this.value = "";
    } else {
        // if (!$.trim('' + this.value).isEmpty()) {
            // if (!currentChannel.isOpenChannel()) {
            //     currentChannel.startTyping();
            // }
        // }
    }
});

$('#send').click(function() {
    var text = $.trim($('#chat-input-text').val());
    if (!text.isEmpty()) {
        currentChannel.sendUserMessage(text, '', SendMessageHandler);
        $('#chat-input-text').val('');
    }
});

$('#chat_file_input').change(function () {
    if ($('#chat_file_input').val().trim().length == 0) return;
    var file = $('#chat_file_input')[0].files[0];
    $('.chat-input-file').addClass('file-upload');

    currentChannel.sendFileMessage(file, SendMessageHandler);
});

/***********************************************
 *            // END MESSAGING
 **********************************************/

/***********************************************
 *            SendBird Settings
 **********************************************/
var sb;
var SendMessageHandler;
var isInit = false;

function startSendBird(userId, channelUrl) {
    sb = new SendBird({ appId: appId });

    sb.connect(userId, function(user, error) {
        if (error) {
            console.error(error);
            return;
        }
        initPage(user);
    });

    var initPage = function(user) {
        isInit = true;
        // $('.init-check').hide();
        currentUser = user;
        nickname = user.nickname;

        sb.GroupChannel.getChannel(channelUrl, function(channel, error) {
            if (error) {
                console.error(error);
                return;
            }
            currentChannel = channel;
            loadPrevMessages(channel);
            channel.markAsRead();
        });
    };

    var loadPrevMessages = function() {
        var messageListQuery = currentChannel.createPreviousMessageListQuery();
        messageListQuery.load(200, false, function(list, error) {
            if (error) {
                console.error(error);
                return;
            }
            list.forEach(function(message) {
                addMessage(message);
            });
            messageList = list;
        });
    };

    var ConnectionHandler = new sb.ConnectionHandler();
    ConnectionHandler.onReconnectStarted = function(id) {
        console.log('onReconnectStarted');
    };

    ConnectionHandler.onReconnectSucceeded = function(id) {
        console.log('onReconnectSucceeded');
        // if (!isInit) {
        //     initPage();
        // }
      };

  // ConnectionHandler.onReconnectFailed = function(id) {
  //   console.log('onReconnectFailed');
  // };
    sb.addConnectionHandler('uniqueID', ConnectionHandler);

    var ChannelHandler = new sb.ChannelHandler();
    ChannelHandler.onMessageReceived = function(channel, message) {
        channel.refresh(function() {});

        if (currentChannel.channelUrl == channel.channelUrl) {
            channel.markAsRead();
            addMessage(message);
            //   if (!document.hasFocus())
            //     notifyMessage(channel, message.message);
        }

        checkUnreadMessage(sb, currentUser);
    };

    SendMessageHandler = function(message, error) {
        if (error) {
            if (error.code == 900050) {
                // setSysMessage({'message': 'This channel is freeze.'});
                return;
            } else if (error.code == 900041) {
                // setSysMessage({'message': 'You are muted.'});
                return;
            }
        }

        if (message.isFileMessage()) {
            $('.chat-input-file').removeClass('file-upload');
            $('#chat_file_input').val('');
        }
        addMessage(message);
    };

    // ChannelHandler.onReadReceiptUpdated = function(channel) {
    //     console.log('ChannelHandler.onReadReceiptUpdated: ', channel);
        // updateChannelMessageCacheAll(channel);
    // };

    // ChannelHandler.onTypingStatusUpdated = function(channel) {
    //     console.log('ChannelHandler.onTypingStatusUpdated: ', channel);

        // if (channel == currChannelInfo) {
        //     showTypingUser(channel);
        // }
    // };

  // ChannelHandler.onUserLeft = function (channel, user) {
  //   console.log('ChannelHandler.onUserLeft: ', channel, user);
  //   setSysMessage({'message': '"' + user.nickname + '" user is left.'});
  //
  //   if (channel.isGroupChannel()){
  //     groupChannelListMembersAndProfileImageUpdate(channel);
  //   }
  // };
  //
  // ChannelHandler.onUserExited = function (channel, user) {
  //   console.log('ChannelHandler.onUserExited: ', channel, user);
  // };
  //
  // ChannelHandler.onChannelChanged = function (channel) {
  //   console.log('ChannelHandler.onChannelChanged: ', channel);
  //   if (channel.isGroupChannel()){
  //     groupChannelListMembersAndProfileImageUpdate(channel);
  //   }
  // };

  sb.addChannelHandler('channel', ChannelHandler);
}

function init(userId) {
    var channelUrl = decodeURI(decodeURIComponent(getUrlVars()['channel']));

    // $('.init-check').show();
    startSendBird(userId, channelUrl);
}

var scrollPositionBottom = function() {
  var scrollHeight = $('#chat-messages')[0].scrollHeight;
  $('#chat-messages')[0].scrollTop = scrollHeight;
};

window.onfocus = function() {
  if (currentChannel)
    currentChannel.markAsRead();
};
