var Book = React.createClass({
	render: function() {
		return (
			<div>
				<div>{this.props.book.name}</div>
				<div className="ratings" id={this.props.book.bookid}></div>
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
	    			return <Book key={book.bookid} book={book}/>
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
    				data:[{bookid:"123",name:"good book"},{bookid:"124",name:"bad book"}]
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