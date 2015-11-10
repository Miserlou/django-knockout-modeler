/* The Model */
function {{modelName}}(data) {{% for fieldName in fields %}
    {{fieldName}} = ko.observable(){% if not forloop.last %},{%endif%}{% endfor %}
}

/* The ViewModel */
function {{modelName}}ViewModel() { 
    var self = this;
    self.{{modelName|lower}}s = ko.observableArray({%if data%}{{modelName}}Data{%else%}[]{%endif%});

    /* Adders and Removers */
	self.add{{modelName}} = function({{modelName|lower}}) {
		self.{{modelName|lower}}s.push({{modelName|lower}});
	};
	self.remove{{modelName}} = function({{modelName|lower}}){
		self.{{modelName|lower}}s.remove({{modelName|lower}})
	};

	/* Canonical Sorts */
	self.sort{{modelName}}sAsc = function(){
		self.{{modelName|lower}}s(self.{{modelName|lower}}s().sort(function(a, b) {
			return a.{{comparator}}>b.{{comparator}}?-1:a.{{comparator}}<b.{{comparator}}?1:0;
		 }));
	};
	self.sort{{modelName}}sDesc = function(){
		self.{{modelName|lower}}s(self.{{modelName|lower}}s().sort(function(a, b) {
			return a.{{comparator}}<b.{{comparator}}?-1:a.{{comparator}}>b.{{comparator}}?1:0;
		}));
	};

	/* Arbitrary Sorts */
	self.sortOnAttributeAsc = function(attribute){
		self.{{modelName|lower}}s(self.{{modelName|lower}}s().sort(function(a, b) {
		  return a[attribute]>b[attribute]?-1:a[attribute]<b[attribute]?1:0;
		}));
	};

	self.sortOnAttributeDescAsc = function(attribute){
		self.{{modelName|lower}}s(self.{{modelName|lower}}s().sort(function(a, b) {
		  return a[attribute]<b[attribute]?-1:a[attribute]>b[attribute]?1:0;
		}));
	};
}