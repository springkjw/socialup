var appId = '68C1D6E3-BFC1-4B8E-B11C-6B1FBE0D3AAA';
// var appId = '4ADA43B7-3F6B-4F5D-BD82-4B629778BE26'; // TEST

/***********************************************
 *               General Purpose
 **********************************************/

/***
 * Python의 format()과 같은 기능을 String class에 추가
 * @returns {string}
 */
String.prototype.format = function () {
  var i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
};

/**
 * 빈 문자열인가?
 * @returns {boolean}
 */
String.prototype.isEmpty = function() {
  return !!(this == null || this == undefined || this.length == 0);
};

/**
 * 숫자를 문자열로 변환하되 반드시 두 글자 이상이 되도록 만듦. eg. 1 -> '01'
 * @param digit
 */
function twoDigitString(digit) {
    return digit < 10 ? '0' + digit : '' + digit;
}

/**
 * ms 단위 integer로 된 시간을 날짜 문자열로 변환 (물론 한국식으로..)
 * @param time
 * @returns {string}
 */
function getDateString(time) {
    var date = new Date(time);
    return '{}.{}.{}'.format(
        date.getFullYear(), twoDigitString(date.getMonth() + 1), twoDigitString(date.getDate()));
}

/**
 * ms 단위 integer로 된 시간을 시간 문자열로 변환
 * @param time
 * @returns {string}
 */
function getTimeString(time) {
    var date = new Date(time);
    return '{}:{}'.format(twoDigitString(date.getHours()), twoDigitString(date.getMinutes()));
}

/**
 * ms 단위의 integer 시간들 사이의 날짜 차이를 리턴
 * @param time1 ms 단위의 시간
 * @param time2 ms 단위의 시간
 */
function diffInDay(time1, time2) {
    var timeDiff = Math.abs(time2 - time1);
    return Math.floor(timeDiff / (1000 * 3600 * 24));
}

/**
 * GET 메소드로 넘어온 파라미터들을 array of hash 형태로 리턴
 * @returns {Array}
 */
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

/***********************************************
 *           END OF General Purpose
 **********************************************/



/***********************************************
 *              Project Specific
 **********************************************/
/**
 * macOS 등 notification을 지원하는 환경을 위한 설정
 */
function notifyMe() {
}

function setCookieUserId(uuid) {
  document.cookie = "user_id=" + uuid + '; expires=Fri, 31 Dec 9999 23:59:59 GMT';
  return uuid;
}

function checkUserId(userId) {
  if (!userId) {
    userId = getUserId();
  } else {
    setCookieUserId(userId);
  }

  if (userId.trim().length == 0) {
    userId = generateUUID();
  }

  return userId;
}

function getUserId() {
  var name = 'user_id=';
  var ca = document.cookie.split(';');
  for (var i=0 ; i<ca.length ; i++) {
    var c = ca[i];
    if (!c) continue;
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) == 0) {
      return c.substring(name.length,c.length);
    }
  }
  return '';
}

function isCurrentUser(userId) {
    return (getUserId()==userId) ? true : false;
}

/**
 * header에 읽지 않은 메시지 수를 표시 (+ SendBird에 사용자가 등록되어 있지 않다면 정보 등록)
 */
function getUnreadMessageCount(userId, nickname, profileUrl) {
    var sb = new SendBird({ appId: appId });
    sb.connect(userId, function(user, error) {
        if (error) {
            console.error(error);
            return;
        }
        checkUnreadMessage(user);
    });

    var checkUnreadMessage = function(user) {
        // SendBird에 이름과 사진 등록..
        if (user.nickname != nickname) {
            sb.updateCurrentUserInfo(nickname, profileUrl, function(response, error) {
                console.log(response, error);
            });
        }

        var unreadCount = 0;
        var channelListQuery = sb.GroupChannel.createMyGroupChannelListQuery();
        channelListQuery.limit = 100;
        channelListQuery.includeEmpty = false;
        if (channelListQuery.hasNext) {
            channelListQuery.next(function(channelList, error) {
                if (error) {
                    console.error(error);
                    return;
                }
                channelList.forEach(function(channel) {
                    unreadCount += channel.unreadMessageCount;
                });
                $('.unread-message-counter').html('<strong>(' + unreadCount + ')</strong>');
                if ($('.unread-message'))
                    $('.unread-message').html('' + unreadCount);
            });
        }

        setTimeout(function() {
            sb.disconnect();
        }, 3 * 1000);
    };
}

/** 해당 유저가 SendBird에 등록되어 있지 않다면 등록..
 * (SendBird API로 특정 유저 업데이트가 안 되서 우회적으로.ㅠㅠ)
 */
function checkOrCreateUser(userId, nickname, profileUrl) {
    var sb = new SendBird({ appId: appId });
    sb.connect(userId, function(user, error) {
        if (error) {
            console.error(error);
            return;
        }
        if (user.nickname != nickname) {
            console.log('Registering seller.. {},{},{}'.format(userId, nickname, profileUrl));
            sb.updateCurrentUserInfo(nickname, profileUrl, function(response, error) {
                console.log(response, error);
            });
        }
        sb.disconnect();
    });
}

/**
 * targetId와의 대화 채널 생성
 */
function openChannel(sb, userId, targetId, cb) {
    var userIds = [userId, targetId];
    sb.GroupChannel.createChannelWithUserIds(userIds, true, function(channel, error) {
        if (error) {
            console.error(error);
            return;
        }
        console.log(channel); // TEST
        cb(channel.url);
    });
}

function startMessage(userId, targetId, targetNickname, targetProfileUrl) {
    // 판매자가 SB에 등록되어 있는지 확인 -> 없으면 등록
    checkOrCreateUser(targetId, targetNickname, targetProfileUrl);

    var channelUrl = '';
    var sb = new SendBird({ appId: appId });
    sb.connect(userId, function(user, error) {
        if (error) {
            console.error(error);
            return;
        }
        channelUrl = openChannel(sb, userId, targetId, function(channelUrl) {
            // message room으로 redirect
            if (!channelUrl.isEmpty())
                window.location.href = '/messages/room/?channel=' + channelUrl;
        });
        sb.disconnect();
    });
}
