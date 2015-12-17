var Book = React.createClass({
	render: function() {
		return (
			<div>
				<div>{this.props.book[0]}</div>
				<div className="ratings" id={this.props.book[6]}></div>
			</div>
		);
	},
});


var BookList = React.createClass({
	getInitialState: function() {
	    return {loading: true};
	},
	render: function() {
		if (this.state.loading) {
			return (
					<div>
					 	Loading Recommendation Lcolumn
					</div>
				);
	    }
		
	    return (
	       <div className="container">
	    	{
	    		this.state.data.map(function(book) {
	    			return <Book key={book[6]} book={book}/>
	    		})
	    	}
	       </div>
	    );
	},
	
     componentDidMount : function() {
    	 $.get("getRecommendation", function(result) {
    		 this.setState(
    			{
    				loading: false,
    				data: JSON.parse(result)
    			}
    		);
        }.bind(this));
	 },
	 componentDidUpdate : function() {
		$('.ratings').raty({	number: 10 ,
 	 						 	click: function(score, evt) {
    								$.post("rate",{ bookid: this.id, score: score });
  							 	}
							});
	 },
});

ReactDOM.render(
		<BookList/>,
		document.getElementById('recommendList')
	);