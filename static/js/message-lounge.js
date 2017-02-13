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

// var isInit = false;
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

    var channelHandler = new sb.ChannelHandler();
    channelHandler.onMessageReceived = function(channel) {
        channel.refresh(function() {});
        initPage(currentUser);
        checkUnreadMessage(sb);
        updateChannelListAll();
    };
    sb.addChannelHandler('channel', channelHandler);
}

var initPage = function(user) {
    // isInit = true;
    // $('.init-check').hide();

    currentUser = user;

    channelListQuery = sb.GroupChannel.createMyGroupChannelListQuery();
    channelListQuery.limit = 100;
    channelListQuery.includeEmpty = true;
    channelListQuery.order = 'latest_last_message';

    allChannels = [];
    unreadChannels = [];
    loadGroupChannelList(false);

    setTimeout(function () {
        updateChannelListAll();
        setInterval(function () {
            updateChannelListAll();
        }, 30 * 1000);
    }, 1000);
};


function init(userId) {
    // $('.init-check').show();
    startSendBird(userId);
}

