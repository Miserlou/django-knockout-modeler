function {{modelName}}(data) {{% for fieldName in fields %}
    {{fieldName}} = ko.observable(){% if not forloop.last %},{%endif%}{% endfor %}
}

function {{modelName}}ViewModel() { 
    var self = this;
    self.{{modelName|lower}}s = ko.observableArray({%if data%}{{modelName}}Data{%else%}[]{%endif%});

	self.add{{modelName}} = function({{modelName|lower}}) {
		self.{{modelName|lower}}s.push({{modelName|lower}});
	};
	self.remove{{modelName}} = function({{modelName|lower}}){
		self.{{modelName|lower}}s.remove({{modelName|lower}})
	};
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
}
