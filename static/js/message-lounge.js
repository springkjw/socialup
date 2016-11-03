var nickname = null;
var userId = null;
var currentUser = null;


/***********************************************
 *                MESSAGING
 **********************************************/

function updateGroupChannelLastMessage(message) {
    var lastMessage = '';
    if (message) {
        lastMessage = message.message;

        lastMessageDateString = '{}<br>{}'.format(getDateString(message.createdAt),
            getTimeString(message.createdAt));

        // TODO: last message가 file인 경우의 처리..

        $('.channel-group[data-channel-url=' + message.channelUrl + '] .channel-lastmessage').html(lastMessage);
        $('.channel-group[data-channel-url=' + message.channelUrl + '] .channel-lastmessagetime').html(lastMessageDateString);
    }
}

function updateGroupChannelListAll(){
  for (var i in groupChannelLastMessageList) {
    var message = groupChannelLastMessageList[i];
    updateGroupChannelLastMessage(message);
  }
}

function addGroupChannel(receiver, targetChannel) {
    groupChannelLastMessageList[targetChannel.url] = targetChannel.lastMessage;

    var lastMessage = targetChannel.lastMessage;
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

function getGroupChannelList() {
    channelListQuery.next(function(channels, error) {
        if (error) {
            return;
        }

        channels.forEach(function(channel) {
            console.log(channel);
            console.log('channel.members'); // TEST
            console.log(channel.members); // TEST

            var receiver = null;
            if (channel.memberCount > 1) {
                receiver = channel.members.find(function(member) {
                    return member.userId != currentUser.userId;
                });
            }
            addGroupChannel(receiver, channel);

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

        $('#channel_list').on('click', 'tr.channel-group', function () {
            window.location.href = '/messages/room?channel=' + $(this).data('channel-url');
        });
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

var channelMessageList = {};
var groupChannelLastMessageList = {};


function startSendBird(userId) {
    sb = new SendBird({
        appId: appId
    });

    sb.connect(userId, function(user, error) {
        if (error) {
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


        getGroupChannelList();

        setTimeout(function () {
            updateGroupChannelListAll();
            setInterval(function () {
                updateGroupChannelListAll();
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
    // getGroupChannelList();

  //   setTimeout(function(){
  //     updateGroupChannelListAll();
  //     setInterval(function(){
  //       updateGroupChannelListAll();
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
  //     updateGroupChannelLastMessage(message);
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

  // ChannelHandler.onMessageDeleted = function (channel, messageId) {
  //   console.log('ChannelHandler.onMessageDeleted: ', channel, messageId);
  // };
  //
  // ChannelHandler.onReadReceiptUpdated = function (channel) {
  //   console.log('ChannelHandler.onReadReceiptUpdated: ', channel);
  //   updateChannelMessageCacheAll(channel);
  // };
  //
  // ChannelHandler.onTypingStatusUpdated = function (channel) {
  //   console.log('ChannelHandler.onTypingStatusUpdated: ', channel);
  //
  //   if (channel == currChannelInfo) {
  //     showTypingUser(channel);
  //   }
  // };
  //
  // ChannelHandler.onUserJoined = function (channel, user) {
  //   console.log('ChannelHandler.onUserJoined: ', channel, user);
  // };
  //
  // ChannelHandler.onUserLeft = function (channel, user) {
  //   console.log('ChannelHandler.onUserLeft: ', channel, user);
  //   setSysMessage({'message': '"' + user.nickname + '" user is left.'});
  //
  //   if (channel.isGroupChannel()){
  //     groupChannelListMembersAndProfileImageUpdate(channel);
  //   }
  // };
  //
  // ChannelHandler.onUserEntered = function (channel, user) {
  //   console.log('ChannelHandler.onUserEntered: ', channel, user);
  // };
  //
  // ChannelHandler.onUserExited = function (channel, user) {
  //   console.log('ChannelHandler.onUserExited: ', channel, user);
  // };
  //
  // ChannelHandler.onUserMuted = function (channel, user) {
  //   console.log('ChannelHandler.onUserMuted: ', channel, user);
  // };
  //
  // ChannelHandler.onUserUnmuted = function (channel, user) {
  //   console.log('ChannelHandler.onUserUnmuted: ', channel, user);
  // };
  //
  // ChannelHandler.onUserBanned = function (channel, user) {
  //   console.log('ChannelHandler.onUserBanned: ', channel, user);
  //   if (isCurrentUser(user.userId)) {
  //     alert('Oops...You got banned out from this channel.');
  //     navInit();
  //     popupInit();
  //   } else {
  //     setSysMessage({'message': '"' + user.nickname + '" user is banned.'});
  //   }
  // };
  //
  // ChannelHandler.onUserUnbanned = function (channel, user) {
  //   console.log('ChannelHandler.onUserUnbanned: ', channel, user);
  //   setSysMessage({'message': '"' + user.nickname + '" user is unbanned.'});
  // };
  //
  // ChannelHandler.onChannelFrozen = function (channel) {
  //   console.log('ChannelHandler.onChannelFrozen: ', channel);
  // };
  //
  // ChannelHandler.onChannelUnfrozen = function (channel) {
  //   console.log('ChannelHandler.onChannelUnfrozen: ', channel);
  // };
  //
  // ChannelHandler.onChannelChanged = function (channel) {
  //   console.log('ChannelHandler.onChannelChanged: ', channel);
  //   if (channel.isGroupChannel()){
  //     groupChannelListMembersAndProfileImageUpdate(channel);
  //   }
  // };
  //
  // ChannelHandler.onChannelDeleted = function (channel) {
  //   console.log('ChannelHandler.onChannelDeleted: ', channel);
  //   deleteChannel(channel);
  // };

  // sb.addChannelHandler('channel', ChannelHandler);
}

function init(userId) {
    // $('.init-check').show();
    startSendBird(userId);
}

function openChannel(receiverId) {
    var groupChannel = null;
    var userIds = [userId, receiverId];

    sb.GroupChannel.createChannelWithUserIds(userIds, true, function(channel, error) {
        if (error) {
            console.error(error);
            return;
        }

        groupChannel = channel;
        console.log(channel);
    });

    return groupChannel;
}

////////////////////////////////////////////////////////////////////////
// TEST
function setup() {
    openChannel('1002');
}

function sendMessage(channel, message) {
    channel.sendUserMessage(message, '', function(message, error) {
        if (error) {
            console.error(error);
            return;
        }
        console.log(message);
    });
}
