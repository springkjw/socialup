var appId = '4ADA43B7-3F6B-4F5D-BD82-4B629778BE26';

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