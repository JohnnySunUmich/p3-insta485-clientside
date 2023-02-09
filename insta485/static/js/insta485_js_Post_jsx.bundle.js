"use strict";
(self["webpackChunkinsta485"] = self["webpackChunkinsta485"] || []).push([["insta485_js_Post_jsx"],{

/***/ "./insta485/js/Post.jsx":
/*!******************************!*\
  !*** ./insta485/js/Post.jsx ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Post)
/* harmony export */ });
/* harmony import */ var _babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/slicedToArray */ "./node_modules/@babel/runtime/helpers/esm/slicedToArray.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__);



var ExampleComponent = /*#__PURE__*/(0,react__WEBPACK_IMPORTED_MODULE_1__.lazy)(function () {
  console.log('Lazy component loaded');
  return Promise.resolve(/*! import() */).then(__webpack_require__.bind(__webpack_require__, /*! ./Post */ "./insta485/js/Post.jsx"));
});
function Post(_ref) {
  var url = _ref.url;
  var _useState = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({}),
    _useState2 = (0,_babel_runtime_helpers_slicedToArray__WEBPACK_IMPORTED_MODULE_0__["default"])(_useState, 2),
    data = _useState2[0],
    setData = _useState2[1];
  (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(function () {
    var ignoreStaleRequest = false;
    fetch(url, {
      credentials: "same-origin"
    }).then(function (response) {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    }).then(function (data) {
      if (!ignoreStaleRequest) setData(data);
    })["catch"](function (error) {
      return console.log(error);
    });
    return function () {
      return ignoreStaleRequest = true;
    };
  }, [url]);
  console.count("Printed");
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", {
    className: "post index"
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_1___default().createElement(ExampleComponent, null));
}
Post.propTypes = {
  url: (prop_types__WEBPACK_IMPORTED_MODULE_2___default().string.isRequired)
};

/***/ })

}]);
//# sourceMappingURL=insta485_js_Post_jsx.bundle.js.map