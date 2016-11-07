var nickname = null;
var userId = null;
var currentUser = null;

/***********************************************
 *                MESSAGING
 **********************************************/

function updateChannelLastMessage(message) {
    if (message) {
        var lastMessage = (message.isFileMessage()) ? message.name : message.message;
        var lastMessageDateString = getDatetimeString(message.createdAt, '<br>');

        $('.channel-group[data-channel-url=' + message.channelUrl + '] .channel-lastmessage').html(lastMessage);
        $('.channel-group[data-channel-url=' + message.channelUrl + '] .channel-lastmessagetime').html(lastMessageDateString);
    }
}

function updateChannelListAll(){
  for (var i in groupChannelLastMessageList) {
    var message = groupChannelLastMessageList[i];
    updateChannelLastMessage(message);
  }
}

function renderChannel(targetChannel) {
    groupChannelLastMessageList[targetChannel.url] = targetChannel.lastMessage;

    var receiver = getReceiverFrom(targetChannel);
    var receiverProfile = (receiver == null) ? '/static/img/no_profile.png' : receiver.profileUrl;
    var receiverName = (receiver == null) ? '(상대가 퇴장하였습니다)' : receiver.nickname;

    $('#channel_list').append(
        '<tr class="channel channel-group" style="cursor:pointer;"' +
        ' data-channel-url="' + targetChannel.url + '">' +
        '<td class="channel-profile"><img src="{}"></td>'.format(receiverProfile) +
        '<td><div class="channel-receiver">{}</div>'.format(receiverName) +
        '<div class="channel-lastmessage"></div></td>' +
        '<td class="channel-lastmessagetime"></td>' +
        '<td><div id="close">' +
            '<div class="cy"></div><div class="cx"></div>' +
        '</div></td>' +
        '</tr>'
    );
}

function getReceiverFrom(channel) {
    var receiver = null;
    if (channel.memberCount > 1) {
        channel.members.forEach(function (member) {
            if (member.userId != currentUser.userId)
                receiver = member;
        });
    }
    return receiver;
}

function loadGroupChannelList(unreadOnly) {
    $('#channel_list').html('');

    // 이미 한 번 읽은 경우..
    if (allChannels.length > 0) {
        if (unreadOnly) {
            unreadChannels.forEach(function(channel) {
                renderChannel(channel);
            });
        }
        else {
            allChannels.forEach(function(channel) {
                renderChannel(channel);
            });
        }

        $('#channel_list').on('click', 'tr.channel-group', function () {
            window.location.href = '/messages/room?channel=' + $(this).data('channel-url');
        });

        updateChannelListAll();
        return;
    }

    channelListQuery.next(function(channels, error) {
        if (error) {
            console.error(error);
            return;
        }

        channels.forEach(function(channel) {
            allChannels.push(channel);
            if (channel.unreadMessageCount > 0)
                unreadChannels.push(channel);

            if ( !(unreadOnly && channel.unreadMessageCount != 0) )
                renderChannel(channel);

            // var targetUrl = channel.url;
            // var unread = channel.unreadMessageCount > 9 ? '9+' : channel.unreadMessageCount;
            // if (unread != 0) {
            //     $.each($('.left-nav-channel'), function(index, item) {
            //         if ($(item).data("channel-url") == targetUrl) {
            //             addUnreadCount(item, unread, targetUrl);
            //         }
            //     });
            // }
        });
    });

    $('#channel_list').on('click', 'tr.channel-group', function () {
        window.location.href = '/messages/room?channel=' + $(this).data('channel-url');
    });
}
/***********************************************
 *            // END MESSAGING
 **********************************************/

/***********************************************
 *            SendBird Settings
 **********************************************/
var sb;
var channelListQuery;

var isInit = false;
var groupChannelLastMessageList = {};
var allChannels = [];
var unreadChannels = [];

function startSendBird(userId) {
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

        channelListQuery = sb.GroupChannel.createMyGroupChannelListQuery();
        channelListQuery.limit = 100;
        channelListQuery.includeEmpty = true;
        channelListQuery.order = 'latest_last_message';

        loadGroupChannelList(false);

        setTimeout(function () {
            updateChannelListAll();
            setInterval(function () {
                updateChannelListAll();
            }, 30 * 1000);
        }, 1000);
    };

  // var ConnectionHandler = new sb.ConnectionHandler();
  // ConnectionHandler.onReconnectStarted = function(id) {
  //   console.log('onReconnectStarted');
  // };

  // ConnectionHandler.onReconnectSucceeded = function(id) {
  //   console.log('onReconnectSucceeded');
  //   if (!isInit) {
  //     initPage();
  //   }
  //
  //   // OpenChannel list reset
  //   if ($('.right-section__modal-bg').is(':visible')) {
  //     var withoutCache = true;
  //     getChannelList(withoutCache);
  //   }
  //
    // GroupChannel list reset
    // channelListQuery = sb.GroupChannel.createMyGroupChannelListQuery();
    // $('#messaging_channel_list').html('');
    // loadGroupChannelList();

  //   setTimeout(function(){
  //     updateChannelListAll();
  //     setInterval(function(){
  //       updateChannelListAll();
  //     }, 1000);
  //   }, 500);
  // };

  // ConnectionHandler.onReconnectFailed = function(id) {
  //   console.log('onReconnectFailed');
  // };
  // sb.addConnectionHandler('uniqueID', ConnectionHandler);

  // var ChannelHandler = new sb.ChannelHandler();
  // ChannelHandler.onMessageReceived = function(channel, message){
  //   var isCurrentChannel = false;
  //
  //   if (currChannelInfo == channel) {
  //     isCurrentChannel = true;
  //   }
  //
  //   channel.refresh(function(){
  //   });
  //
  //   // update last message
  //   if (channel.isGroupChannel()) {
  //     groupChannelLastMessageList[channel.url] = message;
  //     updateChannelLastMessage(message);
  //     moveToTopGroupChat(channel.url);
  //   }
  //
  //   if (isCurrentChannel && channel.isGroupChannel()) {
  //     channel.markAsRead();
  //   } else {
  //     unreadCountUpdate(channel);
  //   }
  //
  //   if (!document.hasFocus()) {
  //     notifyMessage(channel, message.message);
  //   }
  //
  //   if (message.isUserMessage() && isCurrentChannel) {
  //     setChatMessage(message);
  //   }
  //
  //   if (message.isFileMessage() && isCurrentChannel) {
  //     $('.chat-input-file').removeClass('file-upload');
  //     $('#chat_file_input').val('');
  //
  //     if (message.type.match(/^image\/.+$/)) {
  //       setImageMessage(message);
  //     } else {
  //       setFileMessage(message);
  //     }
  //   }
  //
  //   if (message.isAdminMessage() && isCurrentChannel) {
  //     setBroadcastMessage(message);
  //   }
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
  // sb.addChannelHandler('channel', ChannelHandler);
}

function init(userId) {
    // $('.init-check').show();
    startSendBird(userId);
}

