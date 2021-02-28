
class IStockFundamentals():
    
    def get_data(self):
        raise NotImplementedError()

    @property
    def ticker(self):
        raise NotImplementedError()

    @property
    def pe(self):
        raise NotImplementedError()
    
    @property
    def forward_pe(self):
        raise NotImplementedError()

    @property
    def market_cap(self):
        raise NotImplementedError()
    
    @property
    def pb(self):
        raise NotImplementedError()
    
    @property
    def ps(self):
        raise NotImplementedError()

    @property
    def eps(self):
        raise NotImplementedError()
    
    @property
    def forward_eps(self):
        raise NotImplementedError()
    
    @property
    def net_margin(self):
        raise NotImplementedError()

    @property
    def div_yield(self):
        raise NotImplementedError()

    @property
    def div_payout_ratio(self):
        raise NotImplementedError()
    
    @property
    def roe(self):
        raise NotImplementedError()
    
    @property
    def roa(self):
        raise NotImplementedError()
    
    @property
    def interest_coverage(self):
        raise NotImplementedError()

    @property
    def current_ratio(self):
        raise NotImplementedError()

    @property
    def ocf_per_share(self):
        raise NotImplementedError()

    @property
    def short_interest(self):
        raise NotImplementedError()

    @property
    def beta(self):
        raise NotImplementedError()

    


    def to_dataframe(self):
        return pd.DataFrame(
            {
                "Market Cap"                   : self.market_cap,
                "p/e"                          : self.pe,
                "Forward p/e"                  : self.forward_pe,
                "p/b"                          : self.pb,
                "p/s"                          : self.ps,
                "eps"                          : self.eps,
                "Forward eps"                  : self.forward_eps,
                "Net Margin"                   : self.net_margin,
                "ROE"                          : self.roe,
                "ROA"                          : self.roa,
                "Interest Coverage"            : self.interest_coverage,
                "Current Ratio"                : self.current_ratio,
                "Div %"                        : self.div_yield,
                "Payout Ratio"                 : self.div_payout_ratio,
                "Operating Cash Flow per Share": self.ocf_per_share,
                "Short interest"               : self.short_interest,
                "Beta"                         : self.beta,
                # add hystory of earnings, essetsd equity and calculated growth
            },
            index = [self.ticker]
        )
