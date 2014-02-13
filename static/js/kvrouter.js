window.KVrouter = {
		options: {
			hashFormat: '#!',
			interval: true,
		},
		oldHash: location.hash,
		interval: null,
		noHash: true,
		keys: {},
		kvdb: {},
		start: function(options) {

			// check hash automatically when hash changes
			window.addEventListener("hashchange", function() {
				KVrouter.checkHash(); 
			}, false);
			
			// fire up the router by checking current URL
			this.checkHash();
		},
		checkHash: function(h) {

			//return false when hash doesn't match the format
			if (location.hash.substring(0, this.options.hashFormat.length) != this.options.hashFormat) {
				if (!this.noHash) {
					location.reload();
				};
				return false;
			}
			this.noHash = false;

			var hash = h || location.hash.substring(this.options.hashFormat.length);
			var kv = hash.split('&');
			var keyVal = {};

			//call function for the key with the value
			for (i = 0; i < kv.length; i++){
				keyVal[kv[i].split('=')[0]] = kv[i].split('=')[1];
			}
			for (var key in this.kvdb){
				if (!keyVal[key]) {
					delete this.kvdb[key];
				};
			}
			for (var key in keyVal){
				if (typeof(this.keys[key]) != 'undefined' && this.kvdb[key] != keyVal[key]) {
					this.kvdb[key] = keyVal[key];
					this.keys[key](keyVal[key]);
				}
			}
		},	
		// bind function for key in hash
		bind: function(key, callback) {
			this.keys[key] = callback;
		},
		// key-value options
		get: function(key) {

			var hash = location.hash.substring(this.options.hashFormat.length);
			var kv = hash.split('&');
			var keyVal = {};

			//call function for the key with the value
			for (i = 0; i < kv.length; i++){
				keyVal[kv[i].split('=')[0]] = kv[i].split('=')[1];
			}
			return keyVal[key];
		},
		set: function(key, value) {
			var oldVal = this.kvdb[key];
			this.kvdb[key] = value;
			this._generateHash();
			if (typeof(this.keys[key]) != 'undefined') {
				this.keys[key](value);
			};
		},
		remove: function(key) {
			if (!key) return false;
			delete this.kvdb[key];
			this._generateHash();
		},
		clear: function() {
			this.kvdb = {};
			this.keys = {};
			this._generateHash();
		},
		_generateHash: function(){
			var hash = '';
			for (var key in this.kvdb){
				hash +=  key + '=' + this.kvdb[key] + '&';
			};
			location.hash = this.options.hashFormat.substring(1) + hash;
		}
};